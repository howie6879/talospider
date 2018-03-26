#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='talospider',
    version='0.0.3',
    author='Howie Hu',
    description="A simple,lightweight scraping micro-framework",
    author_email='xiaozizayang@gmail.com',
    install_requires=['lxml', 'requests', 'cchardet', 'cssselect'],
    url="https://github.com/howie6879/talospider/blob/master/README.md",
    packages=find_packages(),
    package_data={'talospider': ['utils/*.txt']})
