# -*- coding: utf-8 -*-
"""
`Vorbis`
============
libvorbis wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = 'Vorbis',


class Vorbis(AudioCodec):
    """
    @iblock: (#float) Set noise floor bias for impulse blocks. The value is a
        float number from -15.0 to 0.0. A negative bias instructs the encoder
        to pay special attention to the crispness of transients in the encoded
        audio. The tradeoff for better transient response is a higher bitrate.
    """
    OPT = [
        Opt('c:a', 'codec', value='libvorbis'),
        BoundedOpt('compression_level', cast=float, lower=-15.0, upper=0.0)
    ]
