# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'Pipe', 'PipeIn', 'PipeOut', 'PipeErr',


class Pipe(Protocol):
    """
    `Pipe access protocol`
    ~~~~~~~~~~~~~~~~~~~~~~
    @number: (#bool) 0=stdin, 1=stdout, 2=stderr
    @blocksize: (#str) Set I/O operation maximum block size, in bytes. Default
        value is INT_MAX, which results in not limiting the requested block
        size. Setting this value reasonably low improves user termination
        request reaction time, which is valuable for files on slow medium.

    """
    def __init__(self, *opt, **opts):
        pname = 'i' if str(self.NUMBER) == '0' else ''
        
        super().__init__(
            ByteOpt('blocksize'),
            Opt(pname, 'in_out_err', value='pipe:%s' % self.NUMBER),
            *opt,
            **opts
        )


class PipeIn(Pipe):
    NUMBER = 0


class PipeOut(Pipe):
    NUMBER = 1


class PipeErr(Pipe):
    NUMBER = 2
