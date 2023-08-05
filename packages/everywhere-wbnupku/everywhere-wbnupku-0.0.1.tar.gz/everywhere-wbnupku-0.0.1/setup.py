# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) wbnupku@outlook.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provides.

Filename: setup.py
Authors:  wbnupku(wbnupku@outlook.com)
Date:     2019/04/16 11:19:10
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="everywhere-wbnupku",
    version="0.0.1",
    author="Wang, Xiao",
    author_email="wbnupku@gmail.com",
    description="excecute python code anywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
