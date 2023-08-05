#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import os
from setuptools import setup, find_packages

VERSION = '0.2.2'
DESCRIPTION = ''

long_description = None

if os.path.isfile('README.md'):
    with open('README.md') as f:
        long_description = f.read()

long_description = long_description or DESCRIPTION

setup(
    name = 'fsoopify',
    version = VERSION,
    description = DESCRIPTION,
    long_description = long_description,
    long_description_content_type='text/markdown',
    classifiers = [],
    keywords = ['python', 'fs', 'oop', 'oopify', 'filesystem'],
    author = 'Cologler',
    author_email='skyoflw@gmail.com',
    url = 'https://github.com/Cologler/fsoopify-python',
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    zip_safe = False,
    entry_points = {}
)
