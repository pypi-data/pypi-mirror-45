# -*- coding: utf-8 -*-
"""
`Animated Gif`
==============
"""
from ..cli import *
from ._container import *


__all__ = 'Gif',


class Gif(Container):
    """
    `Gif container format`
    ~~~~~~~~~~~~~~~~~~~~~~
    @loop: (#int) et the number of times to loop the output. Use -1 for no
        loop, 0 for looping indefinitely (default).
    """
    OPT = [
        Opt('f', 'format', value='gif'),
        IntOpt('loop')
    ]
