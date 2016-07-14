#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

import os

def version():
    with open(os.path.abspath('VERSION')) as f:
        return f.read().strip()

    raise IOError("Error: 'VERSION' file not found.")

VERSION = version()

setup(
    name='{project_name}',
    version=VERSION,
    description='{project_description}',
    long_description=open(os.path.abspath('README.md')).read(),
    author='{author}',
    author_email='{email}',
    license='{license}',
    url='{url}',
    packages=find_packages(exclude=[]),
    entry_points={
        'console_scripts': [
            '{entry_point} = {package_name}.{module_name}:main'
        ]
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
