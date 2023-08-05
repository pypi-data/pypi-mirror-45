#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import os
import sys
from setuptools import setup, find_packages, Command
from shutil import rmtree

NAME = "pytesting_utils"
DESCRIPTION = "Utilities for the PyTesting project"
URL = "https://github.com/pytesting/utils"
EMAIL = "python-test-runner@googlegroups.com"
AUTHOR = "Stephan Lukasczyk"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = None

REQUIRED = [
    "virtualenv",
]

EXTRAS = {
    "test": [
        "coverage",
        "pytest",
        "pytest-cov",
    ],
    "dev": [
        "flake8",
        "black",
        "twine",
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

about = {}
if not VERSION:
    project_slug = "pytesting_utils"
    with open(os.path.join(here, project_slug, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package"
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPI via Twine...")
        os.system("twine upload dist/*")

        self.status("Pushing git tags...")
        os.system("git tag -s v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "tests.*",
                                    "*.tests.*"]),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="GNU Lesser General Public License (LGPLv3)",
    keywords="test runner unittest nose pytest",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or "
        "later (LGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
        "Topic :: Education :: Testing",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
        "Topic :: Utilities",
    ],
    test_suite="py.test",
    zip_safe=True,
    cmdclass={
        "upload": UploadCommand,
    },
)
