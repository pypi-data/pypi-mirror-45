# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provides.

Filename: build_air_update.py
Authors:  wangxiao(wangxiao05@baidu.com)
Date:     2018/12/13 14:11:37
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import attr
import typing
from builtins import bytes
from builtins import map


@attr.s
class AirProductFrame(object):
    """Frame."""
    filepath = attr.ib(type=str)
    data = attr.ib(type=bytes)


@attr.s
class AirProductWeightEvent(object):
    """Weigth"""
    samples = attr.ib(type=str)
    cells = attr.ib(type=str)


@attr.s
class AirProductDetectInfo(object):
    """Detect."""
    url = attr.ib(type=str, default='')
    image_data = attr.ib(type=bytes, default=b'')
    left = attr.ib(type=int, default=-1)
    right = attr.ib(type=int, default=-1)
    top = attr.ib(type=int, default=-1)
    bottom = attr.ib(type=int, default=-1)
    tag = attr.ib(type=str, default='')
    score = attr.ib(type=float, default=0.0)
    flag = attr.ib(type=bool, default=False)


@attr.s
class AirRecordOfBuildSearchUpdate(object):
    """Record of event."""
    start_frame = attr.ib(type=AirProductFrame)
    end_frame = attr.ib(type=AirProductFrame)
    goods_num = attr.ib(type=int)
    product_id = attr.ib(type=typing.Text)
    product_name = attr.ib(type=typing.Optional[typing.Text])
    weight = attr.ib(type=AirProductWeightEvent)
    record_id = attr.ib(type=typing.Text)
    detect_info = attr.ib(type=AirProductDetectInfo)

    @staticmethod
    def bytes_to_image(b):
        """Return numpy array."""
        import cv2
        import numpy as np
        imgdata = np.frombuffer(b, dtype='uint8')
        image = cv2.imdecode(imgdata, 1)
        return image

    def with_detected_result(self):
        """Return True is detect_info is returned."""
        if self.detect_info.url:
            return True
        else:
            return False

    def is_filtered(self):
        """Return True if it is filtered."""
        return self.detect_info.flag is False

    def get_crop_image(self):
        """Return ndarray of cropped image."""
        assert not self.is_filtered()
        if self.goods_num > 0:
            imgdata = self.end_frame.data
        else:
            imgdata = self.start_frame.data
        img_arr = AirRecordOfBuildSearchUpdate.bytes_to_image(imgdata)
        x0 = self.detect_info.left
        x1 = self.detect_info.right
        y0 = self.detect_info.top
        y1 = self.detect_info.bottom
        return img_arr[y0: y1, x0: x1]
