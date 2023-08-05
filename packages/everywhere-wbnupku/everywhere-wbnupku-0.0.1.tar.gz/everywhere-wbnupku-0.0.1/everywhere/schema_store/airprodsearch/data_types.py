# -*- coding: utf-8 -*-
"""
This module provides common data types.

Filename: data_types.py
Authors:  wbnupku(wbnupku@gmail.com)
Date:     2018/11/22 15:21:50
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import typing
import builtins
import attr
import numpy as np


@attr.s(cmp=False)
class Feature(object):
    """Feature type."""
    fea_id = attr.ib(type=typing.Text)
    array = attr.ib(type=np.ndarray)

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return False
        if self.fea_id != other.fea_id:
            return False
        if not np.all(self.array.dtype == other.array.dtype):
            return False
        return np.array_equal(self.array, other.array)

    def __ne__(self, other):
        return not self.__eq__(other)


@attr.s
class BoundingBox(object):
    """Bounding box with 2pts."""
    left = attr.ib(type=int)
    right = attr.ib(type=int)
    top = attr.ib(type=int)
    bottom = attr.ib(type=int)


@attr.s
class IndexDetectInfo(object):
    """Including all info for debug."""
    orig_image = attr.ib(type=np.array)
    bbox = attr.ib(type=BoundingBox)


@attr.s
class Brief(object):
    """Brief type."""
    label = attr.ib(type=typing.Text)
    verbose = attr.ib(type=typing.Optional[typing.Any])


@attr.s
class ImageType(object):
    """Represent a 2D image."""
    w = attr.ib(type=int, default=0)
    h = attr.ib(type=int, default=0)
    data = attr.ib(type=builtins.bytes, default=b'')

    def is_empty(self):
        if self.w == 0 or self.h == 0 or not self.data:
            return True
        else:
            return False


@attr.s
class DataInput(object):
    """Object to construct query and search index.

    [description]
    """
    key = attr.ib(type=typing.Text)
    feas = attr.ib(type=typing.List[Feature])
    brief = attr.ib(type=Brief)
    image = attr.ib(type=np.ndarray, default=np.array([0], dtype='uint8'))


@attr.s
class SearchResult(object):
    """Search result by search engine."""
    query_key = attr.ib(type=typing.Text)
    dists = attr.ib(type=np.ndarray)
    inds = attr.ib(type=np.ndarray)
    infos = attr.ib(type=np.ndarray)
