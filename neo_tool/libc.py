# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import ctypes
import ctypes.util
import os


def _errcheck(result, f, args):
    if result == -1:
        errcode = ctypes.get_errno()
        raise OSError(errcode, os.strerror(errcode))
    return result


def load_libc_function(func_name, errcheck=_errcheck):
    """
    加载本地CDLL库
    :param func_name: 方法名称
    :param errcheck: 检查结果是否错误
    :return:
    """
    try:
        libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)
        func = getattr(libc, func_name)
    except AttributeError:
        raise
    if errcheck:
        func.errcheck = errcheck
    return func
