# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Hash', 'Md5', 'FrameHash', 'FrameMd5',


class Hash(Container):
    """
    ``Hash container format``
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    @hash: (#str) Use the cryptographic hash function specified by the
        string algorithm: 'MD5', 'murmur3', 'RIPEMD128', 'RIPEMD160',
        'RIPEMD256', 'RIPEMD320', 'SHA160', 'SHA224', 'SHA256', 'SHA512/224',
        'SHA512/256', 'SHA384', 'SHA512', 'CRC32', 'adler32'
    """
    OPT = [
        Opt('f', 'format', value='hash'),
        OneOfOpt(
            'hash',
            choices=(
                'MD5',
                'murmur3',
                'RIPEMD128',
                'RIPEMD160',
                'RIPEMD256',
                'RIPEMD320',
                'SHA160',
                'SHA224',
                'SHA256',
                'SHA512/224',
                'SHA512/256',
                'SHA384',
                'SHA512',
                'CRC32',
                'adler32'
            )
        )
    ]


class Md5(Container):
    """
    ``MD5 container format``
    """
    OPT = [Opt('f', 'format', value='md5')]


class FrameMd5(Container):
    """
    ``FrameMD5 container format``
    """
    OPT = [Opt('f', 'format', value='framemd5')]


class FrameHash(Hash):
    """
    ``FrameHash container format``
    """
    OPT = [Opt('f', 'format', value='framehash')]
