# -*- coding: utf-8 -*-
"""
`Theora`
============
libtheora wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = ('Theora',)


class Theora(VideoCodec):
    OPT = [Opt('c:v', 'codec', value='libtheora')]
