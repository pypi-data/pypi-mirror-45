# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import open as io_open
from builtins import str

from future import standard_library
standard_library.install_aliases()

__all__ = [
    'compress_data',
    'CHUNK_SIZE'
]

import zlib

from .exceptions import OasisException


CHUNK_SIZE = 5 * 10 ** 8  # 500 Mb


def compress_data(s):
    """
    Compress large data strings.

    Adapted from a StackOverflow.com solution by Dmitry Skryabin

        https://stackoverflow.com/a/36056646/7556955

    with a modification to set block/chunk size to 500 Mb (5 x 10^8 bytes).
    """

    compressed = b''
    begin = 0
    compressor = zlib.compressobj()

    try:
        while begin < len(s):
            compressed += compressor.compress(s[begin:begin + CHUNK_SIZE])
            begin += CHUNK_SIZE

        compressed += compressor.flush()
    except zlib.error as e:
        raise OasisException(str(e))

    return compressed
