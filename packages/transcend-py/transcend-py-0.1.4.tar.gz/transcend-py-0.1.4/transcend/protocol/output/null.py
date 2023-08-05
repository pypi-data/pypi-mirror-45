# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'NullOut',


class NullOut(Protocol):
    """
    `/dev/null output protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """
    def __init__(self, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value='/dev/null'),
            **opts
        )
