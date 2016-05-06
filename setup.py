#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
	name='PyBuddy',
 	version='0.0.1',
	description='',
	author='Tiago Bras',
	author_email='tiagodsbras@gmail.com',
	license='MIT',
	url='',
	packages=find_packages(exclude=[]),
	entry_points={
		'console_scripts': [
			'pybuddy = pybuddy.pybuddy:main'
		]
	}
)
