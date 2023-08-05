# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = ('SftpIn', 'SftpOut')


SFTP_OPT = [IntOpt('timeout'), EnableOpt('truncate'), EnableOpt('private_key ')]


class _Sftp(Protocol):
    """
    `Secure file transfer protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @timeout: (#int) Set timeout in microseconds of socket I/O operations used
        by the underlying low level operation. By default it is set to -1,
        which means that the timeout is not specified.
    @truncate: (#bool) Truncate existing files on write, if set to 1. A value
        of 0 prevents truncating. Default value is 1.
    @private_key: (#str) Specify the path of the file containing private key to
        use during authorization. By default libssh searches for keys in the
        ~/.ssh/ directory.
    """
    OPT = SFTP_OPT


class SftpIn(_Sftp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class SftpOut(_Sftp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
