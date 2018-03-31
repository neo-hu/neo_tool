# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import os
import unittest

from neo_tool.net.md5_socket import get_md5_socket


class TestMd5Socket(unittest.TestCase):

    def runTest(self):
        try:
            s = get_md5_socket()

            print(os.write(s, "11111111211111111111"))
            bin_checksum = os.read(s, 16)
            hex_checksum = ''.join("%02x" % ord(c) for c in bin_checksum)
            print(hex_checksum)
        finally:
            os.close(s)

