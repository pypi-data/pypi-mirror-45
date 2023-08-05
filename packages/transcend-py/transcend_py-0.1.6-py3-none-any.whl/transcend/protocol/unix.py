# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'UnixIn', 'UnixOut',


UNIX_OPT = [IntOpt('timeout'), EnableOpt('listen')]


class _Unix(Protocol):
    """
    `Unix domain sockets`
    ~~~~~~~~~~~~~~~~~~~~~
    @timeout: (#int) Timeout in ms.
    @listen: (#bool) Create the Unix socket in listening mode.
    """
    OPT = UNIX_OPT


class UnixIn(_Unix):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class UnixOut(_Unix):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
