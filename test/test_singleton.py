# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import unittest

from neo_tool.n_file import fallocate
from neo_tool.singleton import singleton

@singleton
class A(object):
    pass


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        f1 = A()
        f2 = A()
        self.assertEqual(f1, f2)
