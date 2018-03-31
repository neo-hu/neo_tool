# coding:utf-8
from __future__ import absolute_import, division, print_function, with_statement

import ctypes
import os
import socket

from neo_tool.libc import load_libc_function

AF_ALG = getattr(socket, 'AF_ALG', 38)

_bound_md5_sockfd = None
_libc_socket = None
_libc_bind = None
_libc_accept = None


class sockaddr_alg(ctypes.Structure):
    _fields_ = [("salg_family", ctypes.c_ushort),
                ("salg_type", ctypes.c_ubyte * 14),
                ("salg_feat", ctypes.c_uint),
                ("salg_mask", ctypes.c_uint),
                ("salg_name", ctypes.c_ubyte * 64)]


def get_md5_socket():
    """
        MD5的socket 描述符，可以用os.write 写数据，然后通过os.read读取checksum
        try:
            s = get_md5_socket()
            os.write(s, "11111111211111111111")
            hex_checksum = ''.join("%02x" % ord(c) for c in os.read(s, 16))
            print(hex_checksum)
        finally:
            os.close(s)

    """
    global _bound_md5_sockfd
    global _libc_socket
    global _libc_bind
    global _libc_accept

    if _libc_accept is None:
        _libc_accept = load_libc_function('accept')
    if _libc_socket is None:
        _libc_socket = load_libc_function('socket')
    if _libc_bind is None:
        _libc_bind = load_libc_function('bind')

    # Do this at first call rather than at import time so that we don't use a
    # file descriptor on systems that aren't using any MD5 sockets.
    if _bound_md5_sockfd is None:
        sockaddr_setup = sockaddr_alg(
            AF_ALG,
            (ord('h'), ord('a'), ord('s'), ord('h'), 0),
            0, 0,
            (ord('m'), ord('d'), ord('5'), 0))
        hash_sockfd = _libc_socket(ctypes.c_int(AF_ALG),
                                   ctypes.c_int(socket.SOCK_SEQPACKET),
                                   ctypes.c_int(0))
        if hash_sockfd < 0:
            raise IOError(ctypes.get_errno(),
                          "Failed to initialize MD5 socket")

        bind_result = _libc_bind(ctypes.c_int(hash_sockfd),
                                 ctypes.pointer(sockaddr_setup),
                                 ctypes.c_int(ctypes.sizeof(sockaddr_alg)))
        if bind_result < 0:
            os.close(hash_sockfd)
            raise IOError(ctypes.get_errno(), "Failed to bind MD5 socket")

        _bound_md5_sockfd = hash_sockfd

    md5_sockfd = _libc_accept(ctypes.c_int(_bound_md5_sockfd), None, 0)
    if md5_sockfd < 0:
        raise IOError(ctypes.get_errno(), "Failed to accept MD5 socket")
    return md5_sockfd
