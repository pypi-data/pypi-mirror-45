# -*- coding: utf-8 -*-
from ..cli import *


__all__ = 'Protocol',


DEFAULT_PROTOCOL_OPT = [
    GroupOpt('protocol_whitelist', 'whitelist', separator=','),
    IntOpt('rw_timeout', 'rw_timeout')
]


class Protocol(OptSet):
    """
    The libavformat library provides some generic global options, which can be
    set on all the protocols. In addition each protocol may support so-called
    private options, which are specific for that component.

    `Protocol`
    ~~~~~~~~~~
    @whitelist (protocol_whitelist): (#tuple(#str)) Set a list of allowed
        protocols.
    @rw_timeout (rw_timeout): (#int) Maximum time to wait for (network) read/write
        operations to complete, in microseconds.
    """
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_PROTOCOL_OPT + self.OPT + list(opt)), **opts)

    def __call__(self, *args, **kwargs):
        return self.__class__(*args, **kwargs)
