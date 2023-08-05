from setuptools import setup

# note we require: windows-curses to run on windows.  how to install just for windows?
__version__ = "0.0.0"  # init this var
with open("./tinycreeper/__version__.py", "r") as v:
    exec(v.read())

setup(
    name="tinycreeper",
    version=__version__,
    description="Easily integrates linters into your projects.",
    author="James Salvatore",
    author_email="jimmy.c.salvatore@gmai.com",
    license="MIT",
    packages=["tinycreeper"],
    install_requires=["Click", "pick", "black"],
    entry_points={"console_scripts": ["tinycreeper=tinycreeper.cli:cli"]},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
