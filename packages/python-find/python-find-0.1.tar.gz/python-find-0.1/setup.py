#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.md', mode='r') as fd:
    long_description = fd.read()

setup(
    name="python-find",
    version="0.1",
    packages=find_packages(),

    author='Andrew Bryant',
    author_email='abryant288@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT'
)
