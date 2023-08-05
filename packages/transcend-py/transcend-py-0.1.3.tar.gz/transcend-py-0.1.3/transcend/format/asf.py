# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Asf',


class Asf(Container):
    """
    `Advanced Systems Format container format`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @packet_size: (#str) Set the muxer packet size. By tuning this setting you
        may reduce data fragmentation or muxer overhead depending on your
        source. Default value is 3200, minimum is 100, maximum is 64k.
    """
    OPT = [
        Opt('f', 'format', value='asf'),
        BitOpt('packet_size')
    ]
