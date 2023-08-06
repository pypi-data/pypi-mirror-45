# -*- coding: utf-8 -*-
"""
`Opus`
============
libopus wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = 'Opus',


class Opus(AudioCodec):
    OPT = [Opt('c:a', 'codec', value='libopus')]
