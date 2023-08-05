# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
###############################################################################
"""
Commonly used tools.

Filename: util.py
Description:
Authors: wangxiao05(wangxiao05@baidu.com)
Date:    2016-03-15 11:07:27
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import inspect
import importlib
import multiprocessing
import time
import logging
import logging.handlers
import sys
import os
import io
import traceback
from io import open
from struct import unpack
import collections
import builtins
from builtins import bytes


import cv2
import numpy as np
from .kvtools import unpack_kv
from .kvtools import KvIter
from .kvtools import append_kv
from .kvtools import traverse_dir


_approotdir = None
_apppath = None
_unittestdatadir = None


VERINFO = sys.version_info


def convert_to_stream_in(s):
    """Convert bytes and files to python 2 and 3 compatable stream."""
    if isinstance(s, str) and s == '-':
        s = sys.stdin
    if isinstance(s, io.IOBase):
        if s.name == '<stdin>':
            return s.buffer
        return s
    if VERINFO.major == 2 and isinstance(s, file):
        return s
    if VERINFO.major == 3 and isinstance(s, bytes):
        return io.BytesIO(s)
    return open(s, 'rb')


def convert_to_stream_out(s, multi_env=False):
    """Convert bytes and files to python 2 and 3 compatable stream."""
    if s is None:
        return None
    if isinstance(s, str) and s == '-':
        s = sys.stdout
    if isinstance(s, io.IOBase):
        if s.name == '<stdout>':
            return s.buffer
        return s
    if VERINFO.major == 2 and isinstance(s, file):
        return s
    if VERINFO.major == 3 and isinstance(s, bytes):
        return io.BytesIO(s)
    return open(s, 'wb')


def pickle_load(fstream):
    """Pickle load."""
    if VERINFO.major == 2:
        import cPickle as pickle
        return pickle.load(fstream)
    else:
        import _pickle as pickle
        return pickle.load(fstream, encoding='bytes')


def pickle_loads(data):
    """Pickle load."""
    if VERINFO.major == 2:
        import cPickle as pickle
        return pickle.loads(data)
    else:
        import _pickle as pickle
        return pickle.loads(data, encoding='bytes')


def pickle_dump(obj, fstream, protocol=2):
    """Pickle dump."""
    if VERINFO.major == 2:
        import cPickle as pickle
        return pickle.dump(obj, fstream)
    else:
        import _pickle as pickle
        return pickle.dump(obj, fstream, protocol=protocol)


def valid_image(imgdata):
    """test if the imgdata is valid, test by loading."""
    img = string_to_cvimage(imgdata)
    if img is not None:
        return True
    else:
        return False


def isfrozen():
    """test frozen module."""
    return hasattr(sys, "frozen")


def parse_kvlist(input_arg, cls=None):
    """Return parsed kvlist."""
    from .attrs_utils import from_bytes
    kvlist = unpack_kv(input_arg)
    if cls is None:
        return [(k, pickle_loads(v)) for k, v in kvlist]
    else:
        return [(k, from_bytes(v, cls)) for k, v in kvlist]


class LogTimer(object):

    def __init__(self):
        self.create_time = LogTimer.get_time()
        self.pre_time = self.create_time

    @staticmethod
    def get_time():
        """Util to return current time in milisecond."""
        from time import time
        return time() * 1000

    def elapse(self, reset=True):
        """Get elasp time."""
        cur_time = LogTimer.get_time()
        pre_time = self.pre_time
        if reset is True:
            self.pre_time = cur_time
        return cur_time - pre_time

    def elapse_mili(self, reset=True):
        """Get elasp time."""
        cur_time = LogTimer.get_time()
        pre_time = self.pre_time
        if reset is True:
            self.pre_time = cur_time
        return int(cur_time - pre_time)

    def duration(self):
        """Get life time."""
        cur_time = LogTimer.get_time()
        pre_time = self.create_time
        return int(cur_time - pre_time)

    def reset(self):
        """Reset timer to current time."""
        self.pre_time = LogTimer.get_time()


def module_path(filepath=''):
    """return module path."""
    if filepath:
        return os.path.abspath(filepath)
    print('module_path:%s' % os.path.abspath(__file__), file=sys.stderr)
    return os.path.abspath(__file__)


def module_dir(filepath=''):
    """Get program dir.

    This will get us the program's directory.
    even if we are frozen using py2exe
    """
    global _approotdir
    if _approotdir is None:
        _approotdir = os.path.dirname(module_path(filepath))
    return _approotdir


def add_module_logger(curmodule):
    """Add module logger and add class logger."""
    if not hasattr(curmodule, 'logger'):
        curmodule.logger = logging.getLogger(curmodule.__name__)
    clsmembers = inspect.getmembers(curmodule, inspect.isclass)
    for clsname, cls in clsmembers:
        try:
            add_class_logger(cls)
        except Exception as e:
            type(e)
            pass  # print "can't add logger to", cls


def add_class_logger(cls):
    """Add class logger."""
    if not hasattr(cls, 'logger'):
        cls.logger = logging.getLogger(cls.__module__ + "." + cls.__name__)


def switch_log_level(log_level):
    """Return the log level parameter."""
    import typing
    if isinstance(log_level, typing.Text):
        log_level = log_level.upper()
        if log_level == 'INFO':
            return logging.INFO
        elif log_level == 'DEBUG':
            return logging.DEBUG
        elif log_level == 'ERROR':
            return logging.ERROR
    elif isinstance(log_level, str):
        log_level = log_level.upper()
        if log_level == b'INFO':
            return logging.INFO
        elif log_level == b'DEBUG':
            return logging.DEBUG
        elif log_level == b'ERROR':
            return logging.ERROR
    return log_level

def setuplogger(logger, logfile=None, LOG_LEVEL=logging.DEBUG):
    """Set up logger."""
    LOG_LEVEL = switch_log_level(LOG_LEVEL)
    if not logfile:  # isfrozen():

        fmt = "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(message)s"
        datefmt = "%m-%d %H:%M:%S"
        logger.setLevel(LOG_LEVEL)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt, datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(LOG_LEVEL)
        logger.addHandler(handler)

    if logfile:
        LOG_FILE = logfile + '.' + str(os.getpid()) + '.log'
        _logdformat = "%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(message)s"
        formatter = logging.Formatter(_logdformat)
        fileLog = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=50000000, backupCount=20)
        fileLog.setLevel(LOG_LEVEL)
        fileLog.setFormatter(formatter)
        # add the handler to the root logger
        mylogger = logging.getLogger('')
        mylogger.addHandler(fileLog)
        mylogger.setLevel(LOG_LEVEL)


def download_img(fp, url, url_prefix=False):
    """Download_img need to test."""
    try:
        import subprocess
        if url_prefix:
            url = 'http://cq02-c1-vis-similar-bstmp1.cq02.baidu.com:8575/image/'\
                + url
        shellcmd = '''
            wget --timeout={0} -t{1} -qO- "{2}" -O "{3}"'''.format(
            500, 3, url, fp)
        subprocess.getoutput(shellcmd)
        return fp
    except:
        return None


globaldebugflag = None
disabledebug = False


def string_to_cvimage(data):
    """Convert bytes to opencv image format."""
    import cv2
    imgdata = np.fromstring(data, dtype='uint8')
    image = cv2.imdecode(imgdata, 1)
    return image


def cvimage_to_string(image, quality=None):
    """Convert opencv image format to bytes."""
    import cv2
    if quality is None:
        dummy, imagedata = cv2.imencode('.jpg', image)
    else:
        dummy, imagedata = cv2.imencode(
            '.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if imagedata is None:
        return None
    else:
        return imagedata.tostring()


def format_cvrect(cvrect):
    """Cvrect to tuple.

    tuple: left, top, width, height
    """
    return '%d,%d,%d,%d' % (cvrect.left, cvrect.top,
                            cvrect.width, cvrect.height)


def ensure_dirs_existence(dir_set):
    """Make dir if not extst.

    Make sure all dirs in dir_set exists, and throw Exceptions if
    any of them not exist
    """
    for dir_path in dir_set:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            assert(os.path.isdir(dir_path))


def import_shared_func(func_path, **kwargs):
    """Import shared func from a dot/slash seperate path.

    import func, object and module by a dot(or slash) joined string
    [func, obj, module] = import_shared_func('module.objct.func')
    """
    import logging
    import importlib
    from functools import partial
    logger = kwargs.get('logger')
    if logger is None:
        logger = logging.getLogger(__name__)
    # logger.debug('Start importing shareed func. func_path: %s' % func_path)
    elems = func_path.split(':')[0].replace('/', '.').split('.')
    args = {}
    arg_items = func_path.split(':')
    if len(arg_items) >= 2:
        args = dict([e.strip().split('=') for e in arg_items[1].split(',')])
    func_name = elems[-1]
    try:
        # logger.debug('Try to import as a func...')
        module = importlib.import_module('.'.join(elems[:-1]))
        func = getattr(module, func_name)
        # logger.debug('Import func succeed. func: %s, module: %s'
        #              % (func.__name__, module.__name__))
        return (partial(func, **args), None, module)
    except:
        # logger.debug('Cannot import as a func. Try to import as an object.')
        try:
            obj_name = elems[-2]
            module = importlib.import_module('.'.join(elems[:-2]))
            obj = getattr(module, obj_name)()
            func = getattr(obj, func_name)
            logger.debug('Import obj succeed. func: %s, obj: %s, module: %s'
                         % (func.__name__, obj.__name__, module.__name__))
            return (partial(func, **args), obj, module)
        except:
            logger.debug('Import as an obj failed. Path: %s' % (func_path, ))
            logger.debug('Fail to import shared func. Path: %s' % func_path)
            raise Exception('Faled to import shared func. Path: %s' % func_path)


def _create_obj(func_path):
    elems = func_path.replace('/', '.').split('.')
    module_path = '.'.join(elems[0:-2])
    class_name = elems[-2]
    func_name = elems[-1]
    module = importlib.import_module(module_path)
    obj = getattr(module, class_name)()
    func = getattr(obj, func_name)
    return (obj, func)


def _get_func(func_path):
    elems = func_path.replace('/', '.').split('.')
    module_path = '.'.join(elems[0:-1])
    func_name = elems[-1]
    module = importlib.import_module(module_path)
    print(module_path)
    func = getattr(module, func_name)
    return func


def _traverse_and_process_image0(input_path, output_dir,
                                 call_func_path, *args):
    call_func = import_shared_func(call_func_path)
    ensure_dirs_existence([output_dir])
    if os.path.isfile(input_path):
        filepaths = [input_path, ]
    else:
        filepaths = traverse_dir(input_path, filter_func=lambda x: 'jpg' in x)
    if len(args) > 0:
        obj_func_path = args[0]
        obj, obj_func = _create_obj(obj_func_path)
    else:
        obj_func = None
    for filepath in filepaths:
        call_func(filepath, output_dir, obj_func)


def get_value_contsign_as_key(k, v):
    """Calc the contsign of v, and return as the new k."""
    cs = calc_contsign(v)
    if cs is None:
        return None
    return (cs, v)


def resize_cvimg(cvimg, ratio=-1):
    """Resize image by ratio.

    If ratio set to -1, the max side length <= 800 strategy
        is used
    """
    img = cvimg.copy()
    H, W = img.shape[:2]
    if ratio < 0:
        t = 800.0 / float(H)
        t2 = 800.0 / float(W)
        t = min(t, t2)
        if t < 1:
            ratio = t
        else:
            ratio = 1.0
    newH = int(ratio * H)
    newW = int(ratio * W)
    res = cv2.resize(img, (newW, newH))
    return res


def resize(imgdata, ratio=-1):
    """Resize imgdata with ratio."""
    cvimg = string_to_cvimage(imgdata)
    resized_cvimg = resize_cvimg(cvimg, ratio)
    return cvimage_to_string(resized_cvimg)


def resize_min(imgdata, width=-1, height=-1):
    """Resize by the specified length of width or height.

    Width is prefered.
    """
    img = string_to_cvimage(imgdata)
    H, W = img.shape[:2]
    assert(width != -1 or height != -1)
    if width != -1:
        ratio = float(width) / float(W)
    else:
        ratio = float(height) / float(H)
    return resize(img, ratio)


def is_sequence(obj):
    """Return if the obj is a sequence."""
    return isinstance(obj, collections.Sequence)


def crop_image(cvimg, r):
    """Crop subimage.

    cvimg is the image of type mat
    r is rect(left, top, width, height)
        or CVRect
    """
    if is_sequence(r):
        return cvimg[r[1]:r[1] + r[3], r[0]:r[0] + r[2], 0:]
    return cvimg[r.top:r.top + r.height, r.left:r.left + r.width, 0:]


def split_input(input_list, split_num):
    """Split input list to split_num of lists."""
    split_num = int(split_num)
    assert(split_num > 0)
    r = len(input_list)
    split_size = r / split_num
    residual = r % split_num
    outputs = []
    offset = 0
    for i in range(0, residual):
        outputs.append(input_list[offset: offset + split_size + 1])
        offset += split_size + 1

    for i in range(residual, split_num):
        outputs.append(input_list[offset: offset + split_size])
        offset += split_size
    print(outputs, file=sys.stderr)
    return outputs


def serialize_call(call_func, inputs, *args):
    """Serailizingly call the call_func iteratinginputs."""
    for inp in inputs:
        call_func(inp, *args)


def serialize_call2(inputs, obj_func_list, pack_func, args):
    """Serailizingly call the func in obj_func_list iterating inputs."""
    for inp in inputs:
        if type(inp) is tuple or type(inp) is list:
            key, val = inp[0: 2]
        else:
            key, val = inp, open(inp).read()
        try:
            all_result = []
            for obj_func in obj_func_list:
                print('calling obj_func %s' % obj_func, file=sys.stderr)
                res = obj_func(val)
                all_result.append(res)
            if len(all_result) == 1:
                pack_input = all_result[0]
            else:
                pack_input = all_result
            print('calling pack_func %s, key:%s, len-res:%d' %
                  (pack_func, key, len(pack_input)), file=sys.stderr)
            pack_func(key, pack_input, *args)
        except Exception as e:
            print(('Exception occured serialize_call2 k:%s, '
                   'v:%d, exception:%s') % (_readable_key(key),
                                            len(val), str(e)), file=sys.stderr)
            traceback.print_exc()
            continue


def traverse_and_process_image_parallel(input_path, call_func_path,
                                        pack_func_path, *args):
    """Parallelly traverse and process.

    Test on caffe gpu, it does not work
        so just set to cpu
    """
    try:
        from caffeimport import caffe
        caffe.set_mode_cpu()
        pass
    except:
        print('import caffe failed. But I dont do anything', file=sys.stderr)

    if type(call_func_path) is str:
        call_func_path_list = call_func_path.split(',')
    else:
        call_func_path_list = call_func_path
    call_func_list = []
    dummy_obj_list = []
    dummy_module_list = []
    for one_call_func_path in call_func_path_list:
        call_func, dummy_obj, dummy_module = \
            import_shared_func(one_call_func_path)
        call_func_list.append(call_func)
        dummy_obj_list.append(dummy_obj)
        dummy_module_list.append(dummy_module)
    # ensure_dirs_existence([output_dir])
    if os.path.isfile(input_path):
        filepaths = [input_path, ]
    else:
        filepaths = traverse_dir(input_path, filter_func=lambda x: 'jpg' in x)
    pack_func, dummy_pack_obj, dummy_pack_module = \
        import_shared_func(pack_func_path)
    print(filepaths)
    for filepath_list in split_input(filepaths, 10):
        # for filepath in filepaths[0:10]:
        if filepath_list:
            # serialize_call2(filepath_list, call_func_list, pack_func, args)
            p = multiprocessing.Process(target=serialize_call2,
                                        args=(filepath_list, call_func_list,
                                              pack_func, args))
            p.start()


def traverse_and_process_image(input_path, call_func_path,
                               pack_func_path, *args):
    """Travese dir, and operate on each file."""
    if type(call_func_path) is str:
        call_func_path_list = call_func_path.split(',')
    else:
        call_func_path_list = call_func_path
    call_func_list = []
    dummy_obj_list = []
    dummy_module_list = []
    for one_call_func_path in call_func_path_list:
        call_func, dummy_obj, dummy_module = \
            import_shared_func(one_call_func_path)
        call_func_list.append(call_func)
        dummy_obj_list.append(dummy_obj)
        dummy_module_list.append(dummy_module)
    # ensure_dirs_existence([output_dir])
    if os.path.isfile(input_path):
        filepaths = [input_path, ]
    else:
        filepaths = traverse_dir(input_path, filter_func=lambda x: 'jpg' in x)
    pack_func, dummy_pack_obj, dummy_pack_module = \
        import_shared_func(pack_func_path)
    for filepath_list in split_input(filepaths, 10):
        # for filepath in filepaths[0:10]:
        if filepath_list:
            serialize_call2(filepath_list, call_func_list, pack_func, args)


def _test_func(msg):
    """Simple test func."""
    for i in range(3):
        print(msg)
        time.sleep(1)


def _my_pyparallel(func, *args):
    for i in range(10):
        msg = "hello %d" % i
        p = multiprocessing.Process(target=_test_func, args=(msg, ))
        p.start()
    print("Sub-process(es) done.", file=sys.stderr)


def _readable_key(key):
    import string
    if isinstance(key, bytes):
        if len(key) == 8:
            return '%s,%s' % unpack('II', key)
        else:
            return key.decode('utf-8')
    elif sys.version_info.major == 2:
        if isinstance(key, unicode):
            return key
        else:
            if all(c in string.printable for c in key):
                return str(key).decode('utf-8')
    else:
        return key


def dummy_func(v):
    """Dummy func for shared_func in process_kv."""
    return v


def dummy_pack(k, v):
    """Dummy pack func for shared_func in process_kv."""
    return k, v


lock = None


def parallel_run(shared_func_path, pack_func_path, logger, input_stream, output_stream, worker_num):
    """Simple parallel call func."""
    from multiprocessing import Process, Queue
    from multiprocessing.queues import Empty
    global lock
    if lock is None:
        lock = multiprocessing.Lock()
    q = Queue()
    if output_stream is None:
        res = Queue()
    else:
        res = output_stream

    def _gen_args(p_ind):
        return [p_ind, q, shared_func_path, pack_func_path, logger, res, True]
    work_func = _process_kv_job_wrapper
    processes = [Process(target=work_func, args=tuple(_gen_args(i))) for i in range(worker_num)]
    for p in processes:
        p.start()

    kviter = KvIter()
    for kv_ind, (k, v) in enumerate(kviter(input_stream)):
        logger.debug('put {} kv in queue. k: {}, v len: {}'.format(kv_ind, repr(k), len(v)))
        q.put((kv_ind, k, v))

    for i in range(worker_num * 2):
        q.put(Sentinal())

    for p in processes:
        p.join()

    if output_stream is None:
        res_list = []
        try:
            while True:
                logger.debug('wait for res q: {}'.format(res.qsize()))

                r = res.get_nowait()
                logger.debug('r type: {}'.format(type(r)))
                res_list.append(res.get_nowait())
        except Empty:
            return res_list
        except Exception as e:
            raise e

    return output_stream


def set_gpu_resource(process_ind):
    from numba import cuda
    try:
        gpu_num = len(cuda.gpus)
    except:
        gpu_num = 0
    if gpu_num > 0 and 'CUDA_VISIBLE_DEVICES' in os.environ:
        visibles = os.environ['CUDA_VISIBLE_DEVICES'].split(',')
        gpu_num = min(gpu_num, len(visibles))

    def _set_caffe_gpu(gpu_num, process_id):
        import caffe
        if gpu_num > 0:
            caffe.set_device(int(process_id) % int(gpu_num))
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()

    _set_caffe_gpu(gpu_num, process_ind)


def _process_kv_job_wrapper(process_ind, q, shared_func_path, pack_func_path, logger, output_stream, multi_env):
    timer = LogTimer()
    timer.reset()
    # process = multiprocessing.current_process()
    pid = os.getpid()
    set_gpu_resource(process_ind)

    if not shared_func_path:
        shared_func = dummy_func
    else:
        shared_func, dummy_obj, dummy_module = \
            import_shared_func(shared_func_path, logger=logger)
        logger.debug('pid:{}. Init {} done! time:{}ms'.format(
            pid, shared_func_path, timer.elapse_mili()))

    if not pack_func_path:
        pack_func = dummy_pack
    else:
        pack_func, dummy_pack_obj, dummy_pack_module = \
            import_shared_func(pack_func_path, logger=logger)
        logger.debug('pid:{}. Init {} done! time:{}ms'.format(
                     pid, pack_func_path, timer.elapse_mili()))

    counter = 0
    while True:
        try:
            timer.reset()
            item = q.get()

            if isinstance(item, Sentinal):
                # logger.debug('pid:{}. kv is sentinal, gonna break. time:{}ms'.format(
                #     pid, timer.elapse_mili()))
                break
            kv_ind, k, v = item
            counter += 1
            # logger.debug('pid:{}. Got the kv. kv_ind:{}, time:{}ms'.format(
            #              pid, kv_ind, timer.elapse_mili(reset=False)))

            i = kv_ind
            input_data = v
            obj_ret = shared_func(input_data)
            pack_ret = pack_func(k, obj_ret)
            if pack_ret is None:
                logger.debug("pid:{} funcs: {} {}, kv_ind:{} k:{} vlen:{}. Processing kv got None! time:{}(ms)"
                             .format(pid, shared_func_path, pack_func_path, i, _readable_key(k), len(v), timer.elapse_mili()))
                continue
            pack_list = []
            if isinstance(pack_ret[0], builtins.bytes):
                # k, v
                pack_list.append(pack_ret[0: 2])
            else:
                # kv list
                pack_list = pack_ret

            for pk, pv in pack_list:
                # logger.debug('pv: {}'.format(pv))
                if pv is not None:
                    if multi_env:
                        if isinstance(output_stream, multiprocessing.queues.Queue):
                            output_stream.put((pk, pv))
                        else:
                            global lock
                            with lock:
                                logger.debug('pid:{} funcs: {} {} kv_ind:{} res_key:{} res_vlen:{}. write to stream {}'.format(
                                    pid, shared_func_path, pack_func_path, kv_ind, pk, len(pv), output_stream))
                                append_kv(pk, pv, output_stream)
                    else:
                        if isinstance(output_stream, list):
                            logger.debug('pid:{} funcs: {} {} kv_ind:{} res_key:{} res_vlen:{}. write to {}'.format(
                                pid, shared_func_path, pack_func_path, kv_ind, pk, len(pv), type(output_stream)))
                            output_stream.append((pk, pv))
                        else:
                            logger.debug('pid:{} funcs: {} {} kv_ind:{} res_key:{} res_vlen:{}. write to {}'.format(
                                pid, shared_func_path, pack_func_path, kv_ind, pk, len(pv), output_stream))

                            append_kv(pk, pv, output_stream)
            logger.debug("pid:{} funcs: {} {} kv_ind:{} k:{} vlen:{}. Process done! time:{}(ms)".format(
                pid, shared_func_path, pack_func_path, kv_ind, _readable_key(k), len(v), timer.elapse_mili()))
        except KeyboardInterrupt:
            logger.info('Terminated manually')
            return
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.warning('Exception occured k:%s, v:%d, exception:%s'
                           % (_readable_key(k), len(v), str(e)),
                           exc_info=True)

    logger.debug("pid:{}. {}, {}. Processing {} kv(s) done! time:{}(ms)"
                 .format(pid, shared_func_path, pack_func_path, counter, timer.duration()))
    return output_stream


class Sentinal(object):
    pass


class KvInputStreamHolder(object):

    def __init__(self, input_stream, multi_env=True):
        global lock
        self.lock = lock
        self.counter = 0
        self.kviter = KvIter(input_stream)

    def get(self):
        try:
            k, v = next(self.kviter())
            kv_ind = self.counter
            self.counter += 1
            return kv_ind, k, v
        except StopIteration:
            return Sentinal()


class KvOutputStreamHolder(object):

    def __init__(self, output_stream, multi_env=False):
        self.counter = 0
        self.stream = output_stream
        global queue
        if multi_env:
            queue = multiprocessing.qu

    def put(self, kv_ind, k, v):
        try:
            k, v = next(self.kviter)
            kv_ind = self.counter
            self.counter += 1
            return kv_ind, k, v
        except:
            return Sentinal()


def process_kv(shared_func_path=None, pack_func_path=None,
               input_arg='-', output_arg='-', logger=None, parallel=1):
    """Used in hadoop kv processing."""

    input_stream = convert_to_stream_in(input_arg)
    output_stream = convert_to_stream_out(output_arg)

    if int(parallel) > 1:
        if logger is None:
            import multiprocessing_logging
            multiprocessing_logging.install_mp_handler()
            logger = logging.getLogger(__name__)
        return parallel_run(shared_func_path, pack_func_path, logger, input_stream, output_stream, parallel)
    else:
        if logger is None:
            logger = logging.getLogger(__name__)
        q = KvInputStreamHolder(input_stream)
        if output_stream is None:
            output_stream = []
        return _process_kv_job_wrapper(0, q, shared_func_path, pack_func_path,
                                       logger, output_stream, multi_env=False)


def image_to_kv(input_path, cs_type='ascii', name_map_file=None):
    """Traverse input_path, and append imgdata as kv to stdout."""
    if cs_type == 'ascii':
        get_contsign = calc_comma_contsign
    else:
        get_contsign = calc_contsign
    if os.path.isfile(input_path):
        filelist = [input_path, ]
    else:
        filelist = traverse_dir(
            input_path, filter_func=lambda x: '.jpg' in x or '.png' in x or '.jpeg' in x)
    filename_map = []
    for filepath in filelist:
        imgdata = open(filepath).read()
        cs = get_contsign(imgdata)
        append_kv(cs, imgdata, sys.stdout)
        filename_map.append('\t'.join((filepath, cs)))
    if name_map_file is not None:
        with open(name_map_file, 'wb') as fout:
            fout.write('\n'.join(filename_map))


def image_to_kvlist(input_path):
    """Traverse input_path, and gen a (contsign, imgdata) list."""
    if os.path.isfile(input_path):
        filelist = [input_path, ]
    else:
        filelist = traverse_dir(input_path, filter_func=lambda x: '.jpg' in x)
    kvlist = []
    for filepath in filelist:
        imgdata = open(filepath).read()
        cs = calc_comma_contsign(imgdata)
        kvlist.append((cs, imgdata))
    return kvlist


def kv_to_image(a, output_dir):
    """Unpack kv data whose value is imadata, and save in output_dir."""
    for cs, imgdata in a:
        key = getasciikey(cs)
        open(output_dir + '/' + key + '.jpg', 'wb').write(imgdata)


def contsignlist_to_kv(filepath, outputpath, pack=False):
    """Convert contsigns in a text file to kv."""
    fout = open(outputpath, 'wb')
    for line in open(filepath):
        val = line.strip()
        if pack:
            val = pack_contsign(val)
        append_kv(val, ' ', fout)
    fout.close()


def contsignlist_to_txt(contsigns, txt_path=None):
    """contsignlist to txt file."""
    import random
    if txt_path is None:
        txt_path = '/tmp/contsigns_to_kv.tmp.' + str(random.randint(0, 100000))
    with open(txt_path, 'wb') as fout:
        fout.write('\n'.join(contsigns))
    return txt_path


def cvrect_to_rect(cvrect):
    """Convert cvrect to rect."""
    return [cvrect.left, cvrect.top, cvrect.width, cvrect.height]


def draw_rects_on_image(imgdata, rects, colors):
    """Draw rects on image."""
    import cv2

    img = string_to_cvimage(imgdata)
    for rect, color in zip(rects, colors):
        x, y, w, h = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)
    return cvimage_to_string(img)


def pack_contsign_as_key_image_as_val(k, v):
    """Calculate contsign of v and pack as kv."""
    from contsign_tool import calc_comma_contsign
    contsign = calc_comma_contsign(v)
    return contsign, v


if __name__ == '__main__':
    if len(sys.argv) > 1:
        func = getattr(sys.modules[__name__], sys.argv[1])
        func(*sys.argv[2:])
    else:
        print(sys.argv[0] + 'cmd [cmd_args]', file=sys.stderr)
