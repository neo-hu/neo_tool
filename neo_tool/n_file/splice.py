# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import ctypes
import os

import operator
import six
import six.moves

from neo_tool.singleton import singleton
from neo_tool.libc import load_libc_function
__all__ = ['Tee', 'Splice']

c_loff_t = ctypes.c_long

# python 2.6 doesn't have c_ssize_t
c_ssize_t = getattr(ctypes, 'c_ssize_t', ctypes.c_long)


@singleton
class Splice(object):
    # From `bits/fcntl-linux.h`
    SPLICE_F_MOVE = 1
    SPLICE_F_NONBLOCK = 2
    SPLICE_F_MORE = 4
    SPLICE_F_GIFT = 8

    __slots__ = '_c_splice'

    def __init__(self):

        def errcheck(result, func, arguments):
            if result == -1:
                errno = ctypes.set_errno(0)
                raise IOError(errno, 'splice: %s' % os.strerror(errno))
            else:
                off_in = arguments[1]
                off_out = arguments[3]

                return (
                    result,
                    off_in.contents.value if off_in is not None else None,
                    off_out.contents.value if off_out is not None else None)
        self._c_splice = load_libc_function("splice", errcheck=errcheck)
        c_loff_t_p = ctypes.POINTER(c_loff_t)
        self._c_splice.argtypes = [
            ctypes.c_int, c_loff_t_p,
            ctypes.c_int, c_loff_t_p,
            ctypes.c_size_t,
            ctypes.c_uint
        ]
        self._c_splice.restype = c_ssize_t

    def __call__(self, fd_in, off_in, fd_out, off_out, len_, flags):

        if not isinstance(flags, six.integer_types):
            c_flags = six.moves.reduce(operator.or_, flags, 0)
        else:
            c_flags = flags

        c_fd_in = getattr(fd_in, 'fileno', lambda: fd_in)()
        c_fd_out = getattr(fd_out, 'fileno', lambda: fd_out)()

        c_off_in = \
            ctypes.pointer(c_loff_t(off_in)) if off_in is not None else None
        c_off_out = \
            ctypes.pointer(c_loff_t(off_out)) if off_out is not None else None
        return self._c_splice(c_fd_in, c_off_in, c_fd_out, c_off_out, len_, c_flags)


@singleton
class Tee(object):
    """Binding to `tee`"""

    __slots__ = '_c_tee',

    def __init__(self):
        self._c_tee = load_libc_function("tee")

        self._c_tee.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_size_t,
            ctypes.c_uint
        ]

        self._c_tee.restype = c_ssize_t

        def errcheck(result, func, arguments):
            if result == -1:
                errno = ctypes.set_errno(0)

                raise IOError(errno, 'tee: %s' % os.strerror(errno))
            else:
                return result

        self._c_tee.errcheck = errcheck

    def __call__(self, fd_in, fd_out, len_, flags):
        """See `man 2 tee`

        File-descriptors can be file-like objects with a `fileno` method, or
        integers.

        Flags can be an integer value, or a list of flags (exposed on
        `splice`).

        This function returns the number of bytes transferred (i.e. the actual
        result of the call to `tee`).

        Upon other errors, an `IOError` is raised with the proper `errno` set.
        """

        if not self.available:
            raise EnvironmentError('tee not available')

        if not isinstance(flags, six.integer_types):
            c_flags = six.moves.reduce(operator.or_, flags, 0)
        else:
            c_flags = flags

        c_fd_in = getattr(fd_in, 'fileno', lambda: fd_in)()
        c_fd_out = getattr(fd_out, 'fileno', lambda: fd_out)()

        return self._c_tee(c_fd_in, c_fd_out, len_, c_flags)
