# coding:utf-8
"""
单例模式
"""
from __future__ import absolute_import, division, print_function, with_statement

import threading


__instance_lock = threading.Lock()


def singleton(cls):
    """

    :param cls:
    :return:
        @Singleton
        class A(object):
            ....
    """
    def _singleton(*args, **kargs):
        if not hasattr(cls, "_instance"):
            with __instance_lock:
                cls._instance = cls(*args, **kargs)
        return cls._instance
    return _singleton


