# -*- coding: UTF-8 -*-
################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
本文件允许模块包以python -m airprodsearch方式直接执行。

Authors: wangxiao05(wangxiao05@baidu.com)
Date:    2018/11/14 13:55:21
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
from .cmdline import pyrun_main
sys.exit(pyrun_main())
