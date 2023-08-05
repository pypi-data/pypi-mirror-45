# -*- coding: utf-8 -*-
"""
`MP3`
============
libmp3lame wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = 'Mp3',


class Mp3(AudioCodec):
    """
    @compression_level: (#int) Set algorithm quality. Valid arguments are
        integers in the 0-9 range, with 0 meaning highest quality but slowest,
        and 9 meaning fastest while producing the worst quality.
    @reservoir: (#bool) Enable use of bit reservoir when set to 1. Default
        value is 1. LAME has this enabled by default.
    @joint_stereo: (#bool) Enable the encoder to use (on a frame by frame basis)
        either L/R stereo or mid/side stereo. Default value is 1.
    @abr: (#bool) Enable the encoder to use ABR when set to 1. The lame --abr
        sets the target bitrate, while this options only tells FFmpeg to use
        ABR still relies on b to set bitrate.
    """
    OPT = [
        Opt('c:a', 'codec', value='libmp3lame'),
        BoundedOpt('compression_level', lower=0, upper=9),
        EnableOpt('reservoir'),
        EnableOpt('joint_stereo'),
        EnableOpt('abr')
    ]
