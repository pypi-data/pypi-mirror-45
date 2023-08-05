# -*- coding: utf-8 -*-
"""
This module provides.

Filename: api_conf.py
Authors:  wbnupku(wbnupku@gmail.com)
Date:     2018/12/26 09:42:10
"""

reload = False
daemon = False
raw_env = []
pidfile = None
workers = 1
max_requests = 10000
max_requests_jitter = 1000
timeout = 600
###################################################################################################
# The default class (sync) should handle most “normal” types of workloads. You’ll want to read
#     Design for information on when you might want to choose one of the other worker classes.
#     Required libraries may be installed using setuptools’ extra_require feature.
#
# sync - default
# eventlet - Requires eventlet >= 0.9.7 (or install it via pip install gunicorn[eventlet])
# gevent - Requires gevent >= 0.13 (or install it via pip install gunicorn[gevent])
# tornado - Requires tornado >= 0.2 (or install it via pip install gunicorn[tornado])
# gthread - Python 2 requires the futures package to be installed (or install it via pip
#           install gunicorn[gthread])
###################################################################################################
worker_class = 'sync'

###################################################################################################
# A comma-separated list of directories to add to the Python path
###################################################################################################
pythonpath = None

###################################################################################################
# logging
###################################################################################################
# accesslog = None
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
# errorlog = '-'
# loglevel = 'info'
# capture_output = False

logger_class = 'gunicorn.glogging.Logger'
logconfig = None
logconfig_dict = {}
bind = ['127.0.0.1:8000']
backlog = 2048


def on_starting(server):
    """Called just before the master process is initialized.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass


def when_ready(server):
    """Called just after the server is started.

    The callable needs to accept a single instance variable for the Arbiter.
    """


def pre_fork(server, worker):
    """Called just before a worker is forked.

    The callable needs to accept two instance variables for the Arbiter and new Worker.
    """
    pass


def post_fork(server, worker):
    """
    Called just after a worker has been forked.

    The callable needs to accept two instance variables for the Arbiter and new Worker.
    """
    pass


def post_worker_init(worker):
    """
    Called just after a worker has initialized the application.

    The callable needs to accept one instance variable for the initialized Worker.

    """
    pass


def worker_int(worker):
    """
    Called just after a worker exited on SIGINT or SIGQUIT.

    The callable needs to accept one instance variable for the initialized Worker.
    """
    pass


def worker_abort(worker):
    """
    Called when a worker received the SIGABRT signal.

    This call generally happens on timeout.

    The callable needs to accept one instance variable for the initialized Worker.
    """
    pass


def pre_exec(server):
    """
    Called just before a new master process is forked.

    The callable needs to accept a single instance variable for the Arbiter.

    """
    pass


def pre_request(worker, req):
    """Called just before a worker processes the request.

    The callable needs to accept two instance variables for the Worker and the Request.
    """
    worker.log.debug("%s %s" % (req.method, req.path))


def post_request(worker, req, environ, resp):
    """
    Called after a worker processes the request.

    The callable needs to accept two instance variables for the Worker and the Request.
    """
    pass


def child_exit(server, worker):
    """
    Called just after a worker has been exited, in the master process.

    The callable needs to accept two instance variables for the Arbiter and the just-exited Worker.

    New in version 19.7.
    """
    pass


def worker_exit(server, worker):
    """
    Called just after a worker has been exited, in the worker process.

    The callable needs to accept two instance variables for the Arbiter and the just-exited Worker.
    """
    pass


def nworkers_changed(server, new_value, old_value):
    """
    Called just after num_workers has been changed.

    The callable needs to accept an instance variable of the Arbiter and two integers of number of workers after and before change.

    If the number of workers is set for the first time, old_value would be None.
    """
    pass


def on_exit(server):
    """
    Called just before exiting Gunicorn.

    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass
