# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provides.

Filename: classify_objects.py
Authors:  wangxiao(wangxiao05@baidu.com)
Date:     2018/11/28 15:22:56
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from time import time
import os
import importlib
import falcon
import pkgutil
import logging
from configobj import ConfigObj
from . import template
from . import attrs_utils as au


class GeneralResource(object):
    """Resource wrapper."""

    def __init__(self, mod, config, logger, init_resource=True):
        self.mod = mod
        self.logger = logger
        if 'RequestJsonObject' in dir(self.mod):
            self.req_type = self.mod.RequestJsonObject
        else:
            req_type = au.create_class_from_json('RequestJsonObject', self.mod.test_cases[0]['req'])
            self.req_type = req_type
        if 'RespJsonObject' in dir(self.mod):
            self.resp_type = self.mod.RespJsonObject
        else:
            resp_type = au.create_class_from_json('RespJsonObject', self.mod.test_cases[0]['resq'])
            self.resp_type = resp_type
        self.config = config
        self.init_resource = init_resource is None or init_resource
        if self.init_resource:
            self.resource = self.mod.Resource(logger=self.logger, **self.config)
        else:
            self.resource = None

    def get_req_from(self, js):
        """Return RequestJsonObject instance."""
        if isinstance(js, dict):
            return au.from_dict(js, self.req_type)
        else:
            return au.from_json(js, self.req_type)

    def get_resp_from(self, js):
        """Return RespJsonObject instance."""
        if isinstance(js, dict):
            return au.from_dict(js, self.resp_type)
        else:
            return au.from_json(js, self.resp_type)

    def get_json_from(self, r):
        """Return a dict from RespJsonObject or RequestJsonObject."""
        if isinstance(r, self.resp_type):
            return au.to_json(r)
        elif isinstance(r, self.req_type):
            return au.to_json(r)
        elif isinstance(r, dict):
            return au.dict_to_json(r)
        else:
            raise TypeError(type(r))

    def on_post(self, req, resp):
        """Define POST method."""
        start_time = time()
        if self.init_resource:
            self.resource = self.mod.Resource(logger=self.logger, **self.config)
        req_json_obj = self.get_req_from(au.dict_from_json_stream(req.bounded_stream))
        resp.body = self.get_json_from(self.resource(req_json_obj))
        resp.status = falcon.HTTP_200
        end_time = time()
        time_used = (end_time - start_time) * 1000
        self.logger.info('module: {} responsed. time:{}ms'.format(self.mod.__name__, time_used))


def create_logger(**kwargs):
    """Create logger for app."""
    logger = kwargs.get('logger')
    if logger is not None:
        return logger
    logger_name = kwargs.get('logger_name')
    logger = logging.getLogger(logger_name)
    if logger_name is not None:
        return logger
    logger.setLevel(logging.DEBUG)
    format = "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s"
    datefmt = "%m-%d %H:%M:%S"
    formatter = logging.Formatter(format, datefmt)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def create_config(**kwargs):
    """Return ConfigObj conf."""
    config_dir = kwargs.get('config_dir')
    config_name = kwargs.get('config_name')
    config = {}
    if config_name is not None and config_dir is not None:
        config = ConfigObj(os.path.join(config_dir, config_name))
    return config


def create_resource(pkg, modname, config, logger, init_resource):
    """Return resource instance and the host module."""
    mod = importlib.import_module(modname, pkg)
    resource = GeneralResource(mod, config, logger, init_resource)
    return resource, mod


def _create_app(root='/restful', config_dir='conf',
                config_name='api.conf', logger=None, *args, **kwargs):
    """Return a falcon api initiated from template module."""
    logger = create_logger(logger=logger)
    config = create_config(config_dir=config_dir, config_name=config_name)
    app = falcon.API()
    package = template
    resource_map = dict()
    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg:
            logger.info('Ignored. Template: {} is a pkg.'.format(modname))
            continue
        try:
            resource, mod = create_resource(package, 'apps.template.' + modname,
                                            config=config, logger=logger,
                                            init_resource=kwargs.get('init_resource')
                                            )
            app.add_route(root + '/' + modname + '/', resource)
            resource_map[root + '/' + modname + '/'] = resource
            logger.info('Succeed. Template: {}.'.format(modname))

        except:
            logger.info('Failed. Template: {} creation.'.format(modname), exc_info=True)
    return app, resource_map


def create_app(*args, **kwargs):
    """Return api."""
    app, _ = _create_app(*args, **kwargs)
    return app
