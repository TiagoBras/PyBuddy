# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division

import sys
import os
import pytest

PROJECT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Insert package directory in the user's PATH
sys.path.insert(0, PROJECT_DIR)

import {package_name}.{module_name} as {module_name}

def test_if_its_working():
    assert 1