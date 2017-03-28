#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

def version():
    with open(os.path.abspath('VERSION')) as f:
        return f.read().strip()
    
    raise IOError("Error: 'VERSION' file not found.")

VERSION = version()

setup(
	name='PyBuddy',
 	version=VERSION,
	description='Creates and setups a well structured Python project',
    long_description=open(os.path.abspath('README.md')).read(),
	author='Tiago Bras',
	author_email='tiagodsbras@gmail.com',
	license='MIT',
	url='https://github.com/TiagoBras/PyBuddy',
	packages=find_packages(exclude=[]),
	entry_points={
		'console_scripts': [
			'pybuddy = pybuddy.cli:main'
		]
	}
)
