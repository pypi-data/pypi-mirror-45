# -*- coding: utf-8 -*-
from ...cli import *
from .._container import *


__all__ = 'Dash',


# https://ffmpeg.org/ffmpeg-formats.html#dash-1

class Dash(Container):
    """
    Dynamic Adaptive Streaming over HTTP (DASH) muxer that creates segments
    and manifest files according to the MPEG-DASH standard
    ISO/IEC 23009-1:2014.

    It creates a MPD manifest file and segment files for each stream.

    The segment filename might contain pre-defined identifiers used with
    SegmentTemplate as defined in section 5.3.9.4.4 of the standard.
    Available identifiers are "$RepresentationID$", "$Number$",
    "$Bandwidth$" and "$Time$".

    Example
    ..
        ffmpeg -re -i <input> -map 0 -map 0 -c:a libfdk_aac -c:v libx264
        -b:v:0 800k -b:v:1 300k -s:v:1 320x170 -profile:v:1 baseline
        -profile:v:0 main -bf 1 -keyint_min 120 -g 120 -sc_threshold 0
        -b_strategy 0 -ar:a:1 22050 -use_timeline 1 -use_template 1
        -window_size 5 -adaptation_sets "id=0,streams=v id=1,streams=a"
        -f dash /path/to/out.mpd
    ..
    """
    OPT = [
        Opt('f', 'format', value='dash'),
        IntOpt('min_seg_duration'),
        IntOpt('window_size'),
        IntOpt('extra_window_size'),
        EnableOpt('remove_at_exit'),
        EnableOpt('use_template'),
        EnableOpt('use_timeline'),
        EnableOpt('single_file'),
        Opt('single_file_name'),
        Opt('init_seg_name'),
        Opt('media_seg_name'),
        Opt('utc_timing_url'),
        KeyValOpt('adaptation_sets'),
    ]
