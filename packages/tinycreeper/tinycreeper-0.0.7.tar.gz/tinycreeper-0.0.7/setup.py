from setuptools import setup

# note we require: windows-curses to run on windows.  how to install just for windows?
version_data = {}
with open("./tinycreeper/__version__.py", "r") as v:
    exec(v.read(), version_data)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tinycreeper",
    version=version_data["__version__"],
    description="Easily integrates linters into your projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="James Salvatore",
    author_email="jimmy.c.salvatore@gmail.com",
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
