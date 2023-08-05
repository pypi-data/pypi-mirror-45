# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) wbnupku@outlook.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provides dict and attrs-like class manipulation method
like jsonpath

Filename: attrpath.py
Authors:  wbnupku(wbnupku@outlook.com)
Date:     2019/01/23 09:35:25
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from typing import Text
import sys
PYTHONVER = sys.version_info.major


def get(obj, p):
    """Get value of obj[p]."""
    if isinstance(p, list):
        fields = p
    else:
        fields = p.split('.')
    ref = obj
    if not fields:
        return obj
    for f in fields:
        if f == '$':
            ref = obj
        elif f == 'this':
            ref = ref
        else:
            if isinstance(ref, list):
                if '=' in f:
                    k, v = f.split('=')
                    flag = False
                    for elem in ref:
                        if isinstance(elem, dict):
                            if elem.get(k) == v:
                                ref = elem
                                flag = True
                                break
                        else:
                            if getattr(elem, k) == v:
                                ref = elem
                                flag = True
                                break
                    if not flag:
                        return None
                else:
                    ref = ref[int(f)]
            elif isinstance(ref, dict):
                ref = ref[f]
            else:
                ref = getattr(ref, f)
    return ref


if PYTHONVER == 2:
    def _type_cast(v, t):
        import base64
        if t == 'str' or t == 'unicode':
            return v.decode('utf-8')
        elif t == 'binary':
            return v
        elif t == 'int':
            return int(v)
        elif t == 'float':
            return float(t)
        elif t == 'base64':
            return base64.b64decode(v)
        else:
            raise TypeError('Not supported type:{}'.format(t))

    def pickle_loads(data):
        """Pickle load."""
        import cPickle as pickle
        return pickle.loads(data)

else:
    def _type_cast(v, t):
        import base64
        if t == 'str' or t == 'unicode':
            return v
        elif t == 'binary':
            return v.encode('utf-8')
        elif t == 'int':
            return int(v)
        elif t == 'float':
            return float(t)
        elif t == 'base64':
            return base64.b64encode(v).decode('utf-8')
        else:
            raise TypeError('Not supported type:{}'.format(t))

    def pickle_loads(data):
        """Pickle load."""
        import _pickle as pickle
        return pickle.loads(data, encoding='bytes')


def get_batch(arg, apath):
    """Return attr value as list."""
    return [get(pickle_loads(e), apath) for e in arg]


def set(obj, p, v, t='str'):
    """set obj[p] to v."""
    if isinstance(p, list):
        fields = p
    else:
        fields = p.split('.')
    ref = get(obj, fields[: -1])
    f = fields[-1]
    if isinstance(ref, list):
        ref[int(f)] = v
    elif isinstance(ref, dict):
        ref[f] = v
    else:
        setattr(ref, f, _type_cast(v, t))
