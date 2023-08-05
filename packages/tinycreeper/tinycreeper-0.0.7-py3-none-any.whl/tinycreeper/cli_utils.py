from pick import pick
import click


def choose_repo_languages():
    """Allows the user to choose multiple languages for their repo.
 
    NOTE: This uses curses which accounts for the screen coloring.
    """

    title = "Pick the languages you'd like to lint in your repo: \n(Hit SPACE to select multiple, ENTER to confirm.)"
    options = ["Python 3.x"]
    selected = pick(options, title, multi_select=True, min_selection_count=1)

    # pick returns a value like [('Lang1', 2), ('Lang4', 5)]; we parse this below.
    selected_languages = [lang for lang in map(lambda x: x[0], selected)]

    return selected_languages
