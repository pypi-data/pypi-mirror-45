# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'RtpIn', 'RtpOut',


class _Rtp(Protocol):
    """
    `Real-time Transport Protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The required syntax for an RTP URL is:
    |rtp://hostname[:port][?option=val...]|
    """


class RtpIn(_Rtp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class RtpOut(_Rtp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
