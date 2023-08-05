import click
from pick import pick
import os
import sys
import json
import re
import subprocess
import shlex

import tinycreeper.cli_utils as cli_utils

LANGUAGE_LINTER = {"Python 3.x": "black", "R": "styler"}
GIT_HOOK_LOCATION = ".git/hooks/pre-commit"


@click.group()
def cli():
    pass


@click.command()
def init():
    if not os.path.isfile(GIT_HOOK_LOCATION):
        click.secho("\n* No pre-commit file found in .git/hooks/.  Adding...", fg="red", bg="white")
        open(GIT_HOOK_LOCATION, "w+")

    languages = cli_utils.choose_repo_languages()
    click.echo("You picked: ")
    for lang in languages:
        click.secho(lang, fg="blue")

    click.secho(f"Currently running in: {os.getcwd()}\n")
    if os.path.isfile(".tinycreeperrc"):
        overwrite = click.confirm(
            "Do you want to overwrite current .tinycreeperrc?", default=True, abort=False
        )

    if not os.path.isfile(".tinycreeperrc") or overwrite:
        with open(".tinycreeperrc", "w+") as tcrc:
            rc_contents = {language: LANGUAGE_LINTER[language] for language in languages}
            json.dump(rc_contents, tcrc)

    user_precommit_choice = click.confirm(
        "Do you want put a git pre-commit hook into the repo?", default=True, abort=False
    )

    # TODO (James): I don't like this section much, I think it can be redone in a nicer way.
    # The gist is to check to see if a config exists: if it doesn't, make one.  If it does, ask
    # the user if they want to replace it.  If so, replace it, if not, leave it alone.
    if user_precommit_choice:

        with open(GIT_HOOK_LOCATION, "r") as precommit:
            precommit_raw = precommit.read()

        previous_tinycreeper_install = re.findall(
            "# TINYCREEPER >>>>.*?# TINYCREEPER <<<<", precommit_raw, re.DOTALL
        )

        if previous_tinycreeper_install:
            click.secho("* You already have a tinycreeper config in your pre-commit hook:\n")
            click.secho("".join(previous_tinycreeper_install))
            user_precommit_choice = click.confirm(
                "\nDo you want to replace your current configuration tinycreeper in pre-commit?",
                default=True,
                abort=False,
            )

            # If the user has a config already but wants to replace it, we remove it here
            # and add it below.

        with open(GIT_HOOK_LOCATION, "w+") as precommit:
            if not previous_tinycreeper_install or user_precommit_choice:
                precommit_changed = re.sub(
                    "[\n]# TINYCREEPER >>>>\n.*?\n# TINYCREEPER <<<<[\n]", "", precommit_raw, re.DOTALL
                )
                print(precommit_changed, file=precommit)
                print("# TINYCREEPER >>>>", file=precommit)
                print("tinycreeper lint", file=precommit)
                print("# TINYCREEPER <<<<", file=precommit)
                os.chmod(GIT_HOOK_LOCATION, 0o775)

        if not user_precommit_choice:
            click.secho("* Making no changes to the pre-commit file, TC already init'ed...")


@click.command()
def lint():
    # TODO: Lint all or lint only committed?  Committed by default.  Put in all.
    if not os.path.isfile(".tinycreeperrc"):
        click.secho("Cannot find .tinycreeperrc.")
        click.secho("Either run from directory root or run `tinycreeper init` from directory root.\n")
        sys.exit(-1)

    config = json.load(open(".tinycreeperrc", "r"))
    for language, linter in config.items():
        click.echo(f"Linting {language} using {linter}...")

        # TODO Gott'a figure a better way to do this.
        if language == "Python 3.x":
            py_suffixes = ["py"]
            cmd = shlex.split(f"black -l 110 {get_committed_files(suffixes=py_suffixes)}")

        elif language == "R":
            pass  # TODO: no idea how to do this one.  Prob just append the files
            # with c(...) or something?

        subprocess.call(cmd)
        re_add_cmd = shlex.split(f"git add {get_committed_files(suffixes=py_suffixes)}")
        subprocess.call(re_add_cmd)


def get_committed_files(suffixes=[]):
    # See: https://git-scm.com/docs/git-diff
    # The diff-filter is: A (added), T (changed), M (modified).
    # This script ONLY gets files which are one of the above.

    # TODO: This only accepts endings which have a single period; nothing like x.tar.gz
    cmd = shlex.split("git diff --name-only --cached --diff-filter=ATM")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    files_committed = [line.decode("UTF-8").strip() for line in p.stdout]
    if suffixes:
        files_committed = [line for line in files_committed if re.findall("[.](.*$)", line)[0] in suffixes]

    files_committed = " ".join(files_committed)
    return files_committed


cli.add_command(init)
cli.add_command(lint)

if __name__ == "__main__":
    cli.run()
