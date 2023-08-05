# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Nut',


class Nut(Container):
    """
    `Nut container format`
    ~~~~~~~~~~~~~~~~~~~~~~
    @syncpoints: (flags)
    @write_index: (#bool) Write index at the end, the default is to write an
        index.
    """
    OPT = [
        Opt('f', 'format', value='nut'),
        FlagsOpt('syncpoints'),
        EnableOpt('write_index')
    ]
