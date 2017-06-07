#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='talonspider',
    version='0.0.1',
    author='Howie Hu',
    description="scraping micro-framework",
    author_email='xiaozizayang@gmail.com',
    install_requires=['lxml', 'requests', 'cchardet', 'cssselect'],
    url="https://github.com/howie6879/talonspider/blob/master/README.md",
    packages=find_packages())
