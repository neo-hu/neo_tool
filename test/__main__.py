# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import os, sys


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)
import unittest

from test.test_n_file import TestFallocate, TestSplice
from test.test_singleton import TestSingleton
from test.test_md5_socket import TestMd5Socket





if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSplice())
    suite.addTest(TestFallocate())
    suite.addTest(TestMd5Socket())
    suite.addTest(TestSingleton("test_singleton"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
