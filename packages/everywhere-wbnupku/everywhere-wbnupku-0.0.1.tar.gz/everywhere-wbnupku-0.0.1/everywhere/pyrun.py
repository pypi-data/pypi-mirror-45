#!/Users/wangxiao05/anaconda3/envs/py36/bin/python
# make executable in bash chmod +x PyRun
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


import sys
import inspect
import importlib
import os
import typing
import builtins
import logging
from io import open
from builtins import input
from copy import deepcopy
from collections import OrderedDict

import attr
from . import attrs_utils as au
from . import kvtools as kv

PYRUN_LOGGER = logging.getLogger('pyrun_logger')
PYRUN_LOGGER.setLevel(logging.INFO)
PYRUN_LOGGER.handlers = [logging.StreamHandler()]
HINT = PYRUN_LOGGER.info


def get_func_args(func):
    """Get arguments of a function."""

    arg_spec = inspect.getargspec(func)
    args = arg_spec.args
    rep = ''
    if len(args) > 0:
        if arg_spec.defaults is not None:
            denum = len(arg_spec.defaults)
            defaults = arg_spec.defaults
        else:
            denum = 0
            defaults = []
        if denum == 0:
            args_nodefault = args[0:]
            args_default = []
        else:
            args_nodefault = args[0: -1 * denum]
            args_default = args[-1 * denum:]
        for arg in args_nodefault:
            rep += '{}: ...\n'.format(arg)
        for arg, d in zip(args_default, defaults):
            rep += '{}: ..., default: {}\n'.format(arg, repr(d))
    if arg_spec.varargs is not None:
        rep += 'varargs arg: {}\n'.format(arg_spec.varargs)
    if arg_spec.keywords is not None:
        rep += 'keywords arg: {}\n'.format(arg_spec.keywords)
    if rep == '':
        rep == 'No args.\n'
        arg_spec = None
    return arg_spec, rep


def _try_to_convert_type(raw, v):
    if v is None:
        return raw
    elif isinstance(v, typing.Text):
        return typing.Text(raw)
    elif isinstance(v, int):
        return int(raw)
    elif isinstance(v, float):
        return float(raw)
    elif isinstance(v, builtins.bytes):
        return builtins.bytes(raw)
    else:
        return raw


class EmptyValue(object):
    pass


def get_func_arg_dict(func):
    arg_spec = inspect.getargspec(func)
    args = arg_spec.args

    arg_dict = OrderedDict()
    if len(args) > 0:
        if arg_spec.defaults is not None:
            denum = len(arg_spec.defaults)
            defaults = arg_spec.defaults
        else:
            denum = 0
            defaults = []
        if denum == 0:
            args_nodefault = args[0:]
            args_default = []
        else:
            args_nodefault = args[0: -1 * denum]
            args_default = args[-1 * denum:]
        for arg in args_nodefault:
            arg_dict[arg] = EmptyValue()
        for arg, d in zip(args_default, defaults):
            arg_dict[arg] = d
    return arg_dict


def hint_func_args(func, prefix):
    """Get arguments of a function."""
    arg_dict = get_func_arg_dict(func)
    for k, v in arg_dict.items():
        if isinstance(v, EmptyValue):
            nv = input(prefix + k + ': ')
            if nv == '':
                HINT('No default value for {}, exit!'.format(k))
                sys.exit(1)
            if nv == "''":
                nv = ''
            if nv != '':
                nv = _try_to_convert_type(nv, v)
            arg_dict[k] = nv
        else:
            nv = input(prefix + k + ': {}(default) '.format(repr(v)))
            if nv == '':
                arg_dict[k] = v
            else:
                if nv == "''":
                    nv = ''
                if nv != '':
                    nv = _try_to_convert_type(nv, v)
                arg_dict[k] = nv
    return arg_dict


def get_fun_list(module):
    """Get module function list."""
    from inspect import getmembers, isfunction
    mod = module
    functions_list = [o for o in getmembers(mod) if isfunction(o[1])]
    return functions_list


def get_time():
    import time
    return str(int(time.time() * 1000))


@attr.s
class CMDManager(object):
    cache_file = attr.ib(type=typing.Text, default=os.path.join(
        os.path.dirname(__file__), '.pyrun_history.kv'))

    def add(self, cmd_rec):
        cmd_bytes = au.to_bytes(cmd_rec)

        with open(self.cache_file, 'ab') as fout:
            kv.append_kv(get_time(), cmd_bytes, fout)

    def get(self, n=10, cmd_rec=None):
        """Get last n histry comands."""
        print('cache file', self.cache_file)
        if not os.path.exists(self.cache_file):
            return []
        if cmd_rec is None:
            cmd_list = list(kv.iter_kv(self.cache_file))[-n:]
            return [(k, au.from_bytes(v, CMDRecord)) for k, v in cmd_list]
        else:
            cmd_list = []
            if not os.path.exists(self.cache_file):
                return cmd_list
            for k, v in kv.iter_kv(self.cache_file):
                cmd_rec_his = au.from_bytes(v, CMDRecord)
                if cmd_rec.module != '' and cmd_rec_his.module == cmd_rec.module \
                        and cmd_rec.obj_entry != '' and cmd_rec_his.obj_entry == cmd_rec.obj_entry:
                    cmd_list.append((k, cmd_rec_his))
            return cmd_list[-1: -n - 1: -1]

    def hint_history(self, cmd_rec, n=3):
        """Get history n commands for hinting."""
        cmd_kv = self.get(n, cmd_rec)
        cmd_dict = {}
        for i, (k, cmd) in enumerate(cmd_kv):
            cmd_dict[i + 1] = cmd
            HINT('[{}] '.format(i + 1) + str(cmd))
        if cmd_kv:
            content = input('Please input cmd index: ')
            if content:
                content = int(content)
                cmd = cmd_dict[content]
                return cmd
        else:
            HINT('No history found!')

    def hint_args(self, cmd_rec, history_num=3):
        """Hint cmd with args."""
        module = importlib.import_module(cmd_rec.module)
        name = cmd_rec.obj_entry
        func_list = get_fun_list(module)
        func = None
        while not hasattr(module, name):
            HINT('Method {} not found in module: {}'.format(name, module))
            HINT('Possible choices...')

            counter = 0
            counter_dict = {}
            prefix = name
            for i, func_info in enumerate(func_list):
                if func_info[0].startswith(prefix):
                    counter += 1
                    counter_dict[counter] = i
                    HINT('  pyrun ' + cmd_rec.module + ' ' +
                         func_info[0] + ' [{}]'.format(counter))
            if not counter_dict:
                HINT('  No method found with prefix: {}'.format(prefix))
                return

            content = input('Index, funcname, or RETURN(exit). prefix[{}]: '.format(prefix))
            if not content:
                HINT('No func is chosen, exit.')
                return

            try:
                num = int(content)
                if num in counter_dict:
                    func_name, func = func_list[counter_dict[num]]
                    name = func_name
                else:
                    HINT('No func is chosen, exit.')
                    return
            except:
                name = content
                for i, func_info in enumerate(func_list):
                    if func_info[0] == name:
                        cmd_rec.obj_entry = name
                        func = func_info[1]
                        break
                if func is not None:
                    break

        cmd_rec.obj_entry = name
        if func is None:
            func = getattr(module, name)

        arg_spec, arg_repr = get_func_args(func)
        HINT('Description:')
        HINT('  func: {}'.format(func))
        func_doc = func.__doc__ if func.__doc__ is not None else ''
        HINT('  doc:\n    ' + func_doc.replace('\n', '\n    '))
        HINT('  args:\n    ' + arg_repr.replace('\n', '\n    '))
        if arg_spec is None:
            return cmd_rec
        hist_cmd_rec = self.hint_history(cmd_rec, history_num)
        if hist_cmd_rec is not None:
            return hist_cmd_rec
        HINT('Complete the cmd:')
        arg_dict = hint_func_args(func, '  ') if arg_spec is not None else {}
        cmd_rec.entry_args = list(deepcopy(arg_dict).items())
        return cmd_rec

    def hint(self, cmd_rec, n=5):
        """Hint history or args."""
        cmd = self.hint_history(cmd_rec, n)
        if cmd is None:
            cmd = self.hint_args(cmd_rec)
        return cmd

    def print_cmd(self, cmd_rec):
        """Print cmd."""
        flag_s = ''
        s = ''
        if cmd_rec.package:
            m = '{}.{}'.format(cmd_rec.package, cmd_rec.module)
        else:
            m = cmd_rec.module
        for k, v in cmd_rec.entry_args:
            flag_s += '--{} {} '.format(k, v)
            s += str(v) + ' '
        print('flag cmd:')
        print('pyflag {} {} {}'.format(m, cmd_rec.obj_entry, flag_s))
        print('cmd:')
        print('pyrun {} {} {}'.format(m, cmd_rec.obj_entry, s))

    def run(self, cmd_rec):
        """Run cmd_rec and record run time status."""
        import traceback
        if cmd_rec is None:
            return
        run_time = cmd_rec.run_time
        run_time.start_time = get_time()
        if cmd_rec.work_dir not in sys.path:
            sys.path.insert(0, cmd_rec.work_dir)
        try:

            module = importlib.import_module(cmd_rec.module)
            func = getattr(module, cmd_rec.obj_entry)
            res = func(**OrderedDict(cmd_rec.entry_args))
            return res
        except Exception as e:
            run_time.exception = str(e)
            run_time.end_time = get_time()
            traceback.print_exc()
        finally:
            run_time.end_time = get_time()
            if run_time.exception != '':
                run_time.exit_status = 1
                run_time.message = traceback.format_exc()
            self.add(cmd_rec)

    @staticmethod
    def get_record_from_cmdline(args=None):
        """Create CMDRecord from cmdline."""

        import sys
        cmd_rec = CMDRecord()
        if args is None:
            args = sys.argv[1:]
        if len(args) == 0:
            HINT('python -m everywhere MODULE_PATH FUNCNAME')
            return None
        module_name = args[0]
        cmd_rec.work_dir = os.path.realpath(os.path.curdir)
        cmd_rec.module = module_name[: -3] if module_name.endswith('.py') else module_name
        cmd_rec.module = cmd_rec.module.replace('/', '.')
        cmd_rec.obj_entry = args[1] if len(args) > 1 else ''
        if len(args) > 2:
            module = importlib.import_module(cmd_rec.module)
            func = getattr(module, cmd_rec.obj_entry)
            cmd_rec.entry_args = list(get_func_arg_dict(func).items())
            params = args[2:]
            for i in range(len(cmd_rec.entry_args)):
                k, v = cmd_rec.entry_args[i]
                if i < len(params):
                    cmd_rec.entry_args[i] = (k, params[i])
        return cmd_rec


@attr.s
class CMDRunTime(object):
    # finished = attr.ib(type=bool, default=False)
    exception = attr.ib(type=typing.Text, default='')
    exit_status = attr.ib(type=int, default=0)
    message = attr.ib(type=typing.Text, default='')
    start_time = attr.ib(type=int, default=0)
    end_time = attr.ib(type=int, default=0)


@attr.s
class CMDRecord(object):
    work_dir = attr.ib(type=typing.Text, default='')
    package = attr.ib(type=typing.Text, default='')
    module = attr.ib(type=typing.Text, default='')
    obj = attr.ib(type=typing.Text, default='')
    init_args = attr.ib(type=typing.List[typing.Tuple[typing.Text, typing.Any]], default=[])
    obj_entry = attr.ib(type=typing.Text, default='')
    entry_args = attr.ib(type=typing.List[typing.Tuple[typing.Text, typing.Any]], default=[])
    run_time = attr.ib(type=CMDRunTime, default=CMDRunTime())

    def __str__(self):
        c = ''
        # c += 'work_dir: {} '.format(self.work_dir)
        # c += 'package: {} '.format(self.package)
        # c += 'obj: {} '.format(self.obj)
        # c += 'init_args: {}\n'.format(self.init_args)
        # c += 'obj_entry: {}\n'.format(self.obj_entry)
        # c += 'entry_args: {}\n'.format(self.entry_args)
        package = self.package
        init_args = ''
        if self.init_args:
            init_args = '\n      Obj args:'
            for k, v in self.init_args:
                if v == '':
                    init_args += '{}={}'.format(k, "''")
                else:
                    init_args += '{}={}'.format(k, v)
        entry_args = '\n      Args:'
        if self.entry_args:
            print(self.entry_args)
            for k, v in self.entry_args:
                if v == '':
                    entry_args += '\n        {}={}'.format(k, "''")
                else:
                    entry_args += '\n        {}={}'.format(k, v)

        c = 'In {}\npyrun{} {} {} {} {} {}'.format(self.work_dir, package, self.module, self.obj,
                                                   init_args, self.obj_entry, entry_args)
        return c

def add_to_history(cmd):
    """Write to history file."""
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.pyrun_history')
    with open(filepath, 'r', encoding='utf-8') as fin:
        last_cmd = fin.readlines()[-1].rstrip()
        if last_cmd == cmd:

            return
    with open(filepath, 'a', encoding='utf-8') as fout:
        fout.write(cmd + '\n')


def hint_cmd_rec(cmd_rec):
    """Hint what it has in cmd_rec."""
    module = importlib.import_module(cmd_rec.module)
    name = cmd_rec.obj_entry
    if not hasattr(module, name):
        HINT('Method {} not found in module: {}'.format(name, module))
        HINT('Possible choices...')
        func_list = get_fun_list(module)
        counter = 0
        counter_dict = {}
        prefix = name
        for i, func_info in enumerate(func_list):
            if func_info[0].startswith(prefix):
                counter += 1
                counter_dict[counter] = i
                HINT('pyrun ' + ' '.join(sys.argv[1: 2]) + ' ' +
                     func_info[0] + ' [{}]'.format(counter))
        num = input('You can choose by index, or return to exit: ')
        if not num:
            return

    num = int(num)
    if num in counter_dict:
        func_name, func = func_list[counter_dict[num]]
        cmd_rec.obj_entry = func_name
        arg_spec, arg_repr = get_func_args(func)
        HINT('Description:')
        HINT('  func: {}'.format(func))
        func_doc = func.__doc__ if func.__doc__ is not None else ''
        HINT('  doc:\n    ' + func_doc.replace('\n', '\n    '))
        HINT('  args:\n    ' + arg_repr.replace('\n', '\n    '))
        HINT('Complete the cmd:')

        arg_dict = hint_func_args(func, '  ') if arg_spec is not None else OrderedDict()
        cmd_rec.entry_args = deepcopy(arg_dict)
        return cmd_rec



def parse_args():
    """Return arg dict."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hint', action='store_true', help='enable hinting')
    parser.add_argument('--last', action='store_true', help='run the last command')
    parser.add_argument('--cmd', type=str, nargs='*', help='cmd')
    parser.add_argument('--pr', '--print-result', dest='print_result', action='store_true', help='print output')
    parser.add_argument('--log-level', type=str, default='INFO', help='Control the running log level')
    parser.add_argument('--print-cmd', action='store_true', help='print pyrun cmd')
    args = parser.parse_args()
    return args


def parse_argstring(parser, s):
    """Return parsed args from arg string."""
    import shlex
    args = parser.parse_args(shlex.split(s))
    return args


def test_HINT(a, b):
    HINT(a, b)


def main(*args):
    """Unit test."""
    from .util import setuplogger

    manager = CMDManager()
    args = parse_args()
    HINT('args: {}'.format(args))
    if args.last:
        _, cmd_rec = manager.get(1)[0]
        running_logger = logging.getLogger()
        setuplogger(running_logger, LOG_LEVEL=args.log_level)
        if args.print_cmd:
            manager.print_cmd(cmd_rec)
        else:
            ret = manager.run(cmd_rec)
            if args.print_result:
                running_logger.info('pyrun output: {}'.format(ret))

    if args.cmd:
        cmd_rec = manager.get_record_from_cmdline(args.cmd)
        if args.hint:
            cmd_rec = manager.hint(cmd_rec)
        running_logger = logging.getLogger()
        setuplogger(running_logger, LOG_LEVEL=args.log_level)
        if args.print_cmd:
            manager.print_cmd(cmd_rec)
        else:
            ret = manager.run(cmd_rec)
            if args.print_result:
                running_logger.info('pyrun output: {}'.format(ret))


def get_package(path_to_module):
    """Return (work_dir, package_name, module_name)."""

    if path_to_module.endswith('.py'):
        path_to_module[:-3].replace('.', '/').strip()


def test_get_package():
    test_cases = ['everywhere/pyrun.py',
                  'everywhere/pyrun',
                  'everywhere.pyrun',
                  './everywhere/pyrun.py'
                  'everywhere',
                  'pyrun.py',
                  'pyrun',
                  '/data1/wangxiao05/icode/baidu/idl-xteam/airprodsearch/everywhere/pyrun.py',
                  '/data1/wangxiao05/icode/baidu/idl-xteam/airprodsearch/everywhere',
                  ]
    gt = [('', 'everywhere', 'pyrun'),
          ('', 'everywhere', 'pyrun'),
          ('', 'everywhere', 'pyrun'),
          ('', 'everywhere', 'pyrun'),
          ('', 'everywhere', 'pyrun'),
          ('', 'everywhere', None),
          ('', '', 'pyrun'),
          ('', '', 'pyrun'),
          ('/data1/wangxiao05/icode/baidu/idl-xteam/airprodsearch', 'pyrun', 'pyrun'),
          ('/data1/wangxiao05/icode/baidu/idl-xteam/airprodsearch', 'pyrun', None)]


if __name__ == '__main__':
    parse_args()




