# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Null',


class Null(Container):
    """
    `Null container format`
    ~~~~~~~~~~~~~~~~~~~~~~~
    For debugging and benchmarking purposes.
    """
    OPT = [Opt('f', 'format', value='null')]
