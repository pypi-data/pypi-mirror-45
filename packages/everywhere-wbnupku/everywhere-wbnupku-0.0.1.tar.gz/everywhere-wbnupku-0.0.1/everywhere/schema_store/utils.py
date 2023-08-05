# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) wbnupku@outlook.com, Inc. All Rights Reserved
#
################################################################################
"""

This module provides utils to access schema.

Filename: utils.py
Authors:  wbnupku(wbnupku@outlook.com)
Date:     2019/01/15 14:16:11
"""

from importlib import import_module
# import schema_store

def get_class_by_pypath(s):
    """Return class referenced by pypath."""
    par_module_name = '.'.join(s.split('.')[:-1])
    class_name = s.split('.')[-1]
    par_module = import_module(par_module_name)
    m = getattr(par_module, class_name)
    return m


def test_get_class_by_pypath():
    """Describe this func with one line."""
    m = get_class_by_pypath('airprodsearch.data_types.Feature')
    print(type(m))
    print(m)
    return None
