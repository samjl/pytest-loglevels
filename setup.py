#!/usr/bin/env python
from setuptools import setup

setup(
    name="pytest-loglevels",
    version='0.3.0',
    author='Sam Lea',
    author_email='samjlea@gmail.com',
    py_modules=['pytest_loglevels'],
    install_requires=['pytest>=2.8.0'],
    # the following makes a plugin available to pytest
    entry_points={'pytest11': ['loglevels = pytest_loglevels']},
    # custom PyPI classifier for pytest plugins
    classifiers=["Framework :: Pytest"],
)
