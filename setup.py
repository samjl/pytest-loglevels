#!/usr/bin/env python
from setuptools import setup

setup(
    name="pytest-loglevels",
    version='0.0.1',
    py_modules=['pytest_loglevels'],
    install_requires=['pytest>=2.7.0'],
    # the following makes a plugin available to pytest
    entry_points={'pytest11': ['loglevels = pytest_loglevels']},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
