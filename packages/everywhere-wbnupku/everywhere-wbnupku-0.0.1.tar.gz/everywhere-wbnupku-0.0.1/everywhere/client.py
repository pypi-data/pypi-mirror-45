# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provides.

Filename: client.py
Authors:  wangxiao(wangxiao05@baidu.com)
Date:     2018/11/29 08:38:01
"""

import requests


def post(hostname, port, route, req_json):
    """General client function."""
    url = 'http://{}:{}{}'.format(hostname, port, route)
    resp = requests.post(url, json=req_json)
    if resp.status_code == 200:
        return resp.status_code, resp.json()
    else:
        return resp.status_code, resp.content


if __name__ == '__main__':
    print(post())
