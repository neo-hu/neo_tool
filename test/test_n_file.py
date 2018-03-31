# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import unittest
import os
from tempfile import mkstemp

from neo_tool.n_file import fallocate, splice


def _get_tempfile():
    return mkstemp()


class TestSplice(unittest.TestCase):
    def runTest(self):
        with open("/tmp/_splice.txt", "wb") as f:
            f.write("1234567890")
        s = splice.Splice()
        r, w = os.pipe()
        with open("/tmp/_splice.txt", "rb") as f:
            bytes_in_pipe, _1, _2 = s(f, None, w, None, 51, 0)
            print(bytes_in_pipe)
            with open("/tmp/_splice_w.txt", "wb") as wf:
                print(s(r, None, wf, None, 1024, 0))


class TestFallocate(unittest.TestCase):
    def test_fallocate(self):
        f = fallocate.Fallocate()
        self.assertIsNotNone(f.func_name)
        self.assertIsNotNone(f.fallocate)
        fd, tmp_file = _get_tempfile()
        size = 1024
        try:
            self.assertEqual(f(fd, 0, 0, size), 0)
            self.assertTrue(os.path.exists(tmp_file))
            self.assertEqual(os.path.getsize(tmp_file), size)
        finally:
            os.close(fd)
            try:
                if tmp_file:
                    os.unlink(tmp_file)
            except OSError:
                pass

    def runTest(self):
        self.test_fallocate()
