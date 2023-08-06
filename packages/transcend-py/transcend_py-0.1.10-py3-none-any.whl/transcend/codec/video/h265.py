# -*- coding: utf-8 -*-
"""
`H.265/HEVC`
============
libx265 wrapper for FFMPEG
"""
from ...cli import *
from .h264 import H264


__all__ = 'H265', 'Hevc',


class H265(H264):
    """
    ``H.265-specific Options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    @x265opts: (#dict(key=value)) Set any x265 option, see x265 --fullhelp
        for a list.
    """
    def __init__(self, *opt, **opts):
        super().__init__(
            *([KeyValOpt('x265opts', separator=':')] + list(opt)),
            **opts
        )


Hevc = H265
# nvenc_h265
# nvenc_hevc
# -pixel_format yuv444p
# https://trac.ffmpeg.org/wiki/HWAccelIntro
