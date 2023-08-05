# -*- coding: utf-8 -*-
import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding="utf-8") as f:
        content = f.read()
    return content


README = read_file("README.rst")


ENTRY_POINTS = {"console_scripts": ["debts = debts.cli:main"]}

setup(
    name="debts",
    version="0.1",
    description="Help solve debts settlement.",
    long_description=README,
    license="Custom BSD Beerware",
    classifiers=["Programming Language :: Python :: 3.7"],
    keywords="debts settlement money balance",
    author="Alexis Métaireau & contributors",
    author_email="alexis@notmyidea.org",
    url="https://framagit.com/almet/debts",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points=ENTRY_POINTS,
)
