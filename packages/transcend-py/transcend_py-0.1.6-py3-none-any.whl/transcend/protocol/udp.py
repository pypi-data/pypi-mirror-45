# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'UdpIn', 'UdpOut'


class _Udp(Protocol):
    """
    `User Datagram Protocol`
    """


class UdpIn(_Udp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class UdpOut(_Udp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
