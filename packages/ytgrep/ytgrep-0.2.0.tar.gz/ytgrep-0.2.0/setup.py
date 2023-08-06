#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

with open('README.rst') as f:
    readme = f.read()

setup(
    name='ytgrep',
    version='0.2.0',
    description='CLI tool to search youtube captions',
    long_description=readme,
    author='Alex Kohler',
    author_email='alexjohnkohler@gmail.com',
    license=license,
    packages=find_packages(exclude=('test')),
    py_modules=['ytgrep'],
    entry_points={
        "console_scripts": ['ytgrep = ytgrep:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ]
)
