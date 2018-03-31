# coding:utf-8
# Linux下生成大文件
from __future__ import absolute_import, division, print_function, with_statement

import os
import ctypes
import ctypes.util

import errno
import threading

from neo_tool.libc import load_libc_function
from neo_tool.singleton import singleton


@singleton
class Fallocate(object):

    def __init__(self, check_free=True):
        self.check_free = check_free
        self.func_name = ""
        self.fallocate = ""
        last_error = None
        for func in ('fallocate', 'posix_fallocate'):
            last_error = None
            try:
                self.func_name = func
                self.fallocate = load_libc_function(func)
                break
            except Exception as err:
                last_error = err
        if last_error:
            raise last_error

    def __call__(self, fd, mode, offset, length):
        """
        生成大文件
        :param fd:
        :param mode:
        :param offset:
        :param length:
        :return:

         1, fallocate = Fallocate(False)
            f = open("/tmp/f_test.data", "wb")
            print(fallocate(f, 0, 0, 2 * 1024 * 1024 * 1024))

         2, fallocate = Fallocate.instance()
            f = open("/tmp/f_test.data", "wb")
            print(fallocate(f, 0, 0, 2 * 1024 * 1024 * 1024))
        """

        fd = getattr(fd, "fileno", lambda: fd)()
        if self.check_free:
            st = os.fstatvfs(fd)
            free = st.f_frsize * st.f_bavail - length
            if float(free) <= 0:
                raise OSError(errno.ENOSPC, "fallocate fail free <= 0")
        c_length = ctypes.c_uint64(length)
        args = {
            'fallocate': (fd, mode, offset, c_length),
            'posix_fallocate': (fd, offset, c_length)
        }
        return self.fallocate(*args[self.func_name])


