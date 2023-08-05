import os
import pathlib
import shutil
import sys

from setuptools import find_packages, setup, Command


# Package name.
NAME = "dott"

# Import the README and use it as the long-description
# Note: README.md needs to be in the MANIFEST
here = os.path.abspath(os.path.dirname(__file__))
readme_file = pathlib.Path(here, "README.md")
with readme_file.open() as f:
    readme = f.read()

# Load the package's __version__.py module as a dictionary
about = dict()
with pathlib.Path(here, NAME, "__version__.py").open() as f:
    exec(f.read(), about)


class PublishCommand(Command):
    """Adds support for setup.py publish."""
    description = "Build and publish the package."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print("Removing previous builds…")
            shutil.rmtree(os.path.join(here, "dist"))
        except FileNotFoundError:
            pass
        print("Building Source distribution…")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))
        print("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")
        print("Pushing git tags…")
        os.system("git tag v{0}".format(about.get("__version__")))
        os.system("git push --tags")
        sys.exit()


setup(
    name=NAME,
    version=about.get("__version__"),
    description=about.get("__description__"),
    long_description=readme,
    author=about.get("__author__"),
    author_email=about.get("__email__"),
    url=about.get("__url__"),
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    cmdclass={
        "publish": PublishCommand,
    }
)
