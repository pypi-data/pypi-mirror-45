# -*- coding: utf-8 -*-
from ...cli import *
from .._container import *


__all__ = ('SmoothStreaming',)


class SmoothStreaming(Container):
    """
    Smooth Streaming muxer generates a set of files (Manifest, chunks) suitable
    for serving with conventional web server.


    ``SmoothStreaming muxer options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @window_size: (#int) Specify the number of fragments kept in the manifest.
        Default 0 (keep all).
    @extra_window_size: (#int) Specify the number of fragments kept outside of
        the manifest before removing from disk. Default 5.
    @lookahead_count: (#int) Specify the number of lookahead fragments.
        Default 2.
    @min_frag_duration: (#int) Specify the minimum fragment duration
        (in microseconds). Default 5000000.
    @remove_at_exit: (#int) Specify whether to remove all fragments when
        finished. Default 0 (do not remove).
    """
    OPT = [
        Opt('f', 'format', value='smoothstreaming'),
        IntOpt('window_size'),
        IntOpt('extra_window_size'),
        IntOpt('lookahead_count'),
        IntOpt('min_frag_duration'),
        EnableOpt('remove_at_exit')
    ]
