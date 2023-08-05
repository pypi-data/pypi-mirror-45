# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'Md5Out',


class Md5Out(Protocol):
    """
    `MD5 output protocol.`
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Computes the MD5 hash of the data to be written, and on close writes this
    to the designated output or stdout if none is specified. It can be used to
    test muxers without writing an actual file.
    """
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value='md5:' + endpoint),
            **opts
        )
