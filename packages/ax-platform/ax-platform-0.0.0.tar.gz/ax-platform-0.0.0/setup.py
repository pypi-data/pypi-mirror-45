#!/usr/bin/env python3

from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ax-platform",
    version="0.0.0",
    long_description=long_description,
    long_description_content_type='text/markdown'
)
