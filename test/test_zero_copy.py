# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import os, sys


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASEDIR)

from neo_tool.n_file import fallocate, splice
# f = fallocate.Fallocate()
# with open("/tmp/_fallocate.tmp", "wb") as fd:
#     f(fd, 0, 0, 1024 * 1024 * 600)