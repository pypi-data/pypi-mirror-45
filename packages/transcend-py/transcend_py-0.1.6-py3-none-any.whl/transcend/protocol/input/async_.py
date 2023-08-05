# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'AsyncIn',


class AsyncIn(Protocol):
    """
    `Asynchronous data filling wrapper protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Fill data in a background thread, to decouple I/O operation from demux
    thread.

    async:URL
    async:http://host/resource
    async:cache:http://host/resource
    """
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value='async:' + endpoint),
            **opts
        )
