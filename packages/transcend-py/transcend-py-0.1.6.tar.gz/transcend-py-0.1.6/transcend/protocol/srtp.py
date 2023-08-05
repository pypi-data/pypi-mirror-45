# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'SrtpIn', 'SrtpOut',


class _Srtp(Protocol):
    """
    `Secure Real-time Transport Protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The required syntax for an RTP URL is:
    |rtp://hostname[:port][?option=val...]|
    """


class SrtpIn(_Srtp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class SrtpOut(_Srtp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
