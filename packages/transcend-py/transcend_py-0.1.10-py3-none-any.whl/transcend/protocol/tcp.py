# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'TcpIn', 'TcpOut',


TCP_OPT = [
    EnableOpt('listen'),
    IntOpt('timeout'),
    IntOpt('listen_timeout'),
    ByteOpt('recv_buffer_size'),
    ByteOpt('send_buffer_size')
]


class _Tcp(Protocol):
    """
    `Transmission Control Protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @listen: (#bool) Listen for an incoming connection. Default value is 0.
    @timeout: (#int) Set raise error timeout, expressed in microseconds.
    @listen_timeout: (#int) Set listen timeout, expressed in milliseconds.
    @recv_buffer_size: (#str) Set receive buffer size, expressed bytes.
    @send_buffer_size: (#str) Set send buffer size, expressed bytes.
    """
    OPT = TCP_OPT


class TcpIn(_Tcp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class TcpOut(_Tcp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
