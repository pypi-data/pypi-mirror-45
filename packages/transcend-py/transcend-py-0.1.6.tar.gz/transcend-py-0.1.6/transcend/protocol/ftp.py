# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'FtpIn', 'FtpOut'


FTP_OPT = [
    IntOpt('timeout'),
    Opt('ftp-anonymous-password', 'anonymous_password'),
    EnableOpt('ftp-write-seekable', 'write_seekable'),
    EnableOpt('follow')
]


class _Ftp(Protocol):
    """
    `File transfer protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~
    @timeout: (#int) Set timeout in microseconds of socket I/O operations used
        by the underlying low level operation. By default it is set to -1,
        which means that the timeout is not specified.
    @anonymous_password (ftp-anonymous-password): (#str) Password used when
        login as anonymous user. Typically an e-mail address should be used.
    @write_seekable (ftp-write-seekable): (#bool) Control seekability of
        connection during encoding. If set to 1 the resource is supposed to be
        seekable, if set to 0 it is assumed not to be seekable. Default value
        is 0.
    @follow: (#bool) If set to 1, the protocol will retry reading at the end
        of the file, allowing reading files that still are being written. In
        order for this to terminate, you either need to use the rw_timeout
        option, or use the interrupt callback (for API users).
    """
    OPT = FTP_OPT


class FtpIn(_Ftp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class FtpOut(_Ftp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
