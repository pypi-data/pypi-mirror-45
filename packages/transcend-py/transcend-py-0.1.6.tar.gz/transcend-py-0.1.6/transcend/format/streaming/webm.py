# -*- coding: utf-8 -*-
from ...cli import *
from .._container import *


__all__ = ('WebMDash', 'WebMChunk')


class WebMDash(Container):
    """
    This muxer implements the WebM DASH Manifest specification to generate the
    DASH manifest XML. It also supports manifest generation for DASH live
    streams.


    ``WebM DASH Manifest muxer options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @adaptation_sets: (#str) "id=x,streams=a,b,c id=y,streams=d,e" where x and
        y are the unique identifiers of the adaptation sets and a,b,c,d and e
        are the indices of the corresponding audio and video streams. Any number
        of adaptation sets can be added using this option.
    @live: (#bool) Set this to 1 to create a live stream DASH Manifest.
        Default: 0.
    @chunk_start_index: (#int) Start index of the first chunk. This will go in
        the ‘startNumber’ attribute of the ‘SegmentTemplate’ element in the
        manifest. Default: 0.
    @chunk_duration (chunk_duration_ms): (#int) Duration of each chunk in
        milliseconds. This will go in the ‘duration’ attribute of the
        ‘SegmentTemplate’ element in the manifest. Default: 1000.
    @utc_timing_url: (#str) URL of the page that will return the UTC timestamp
        in ISO format. This will go in the ‘value’ attribute of the ‘UTCTiming’
        element in the manifest. Default: None.
    @time_shift_buffer_depth: (#int) Smallest time (in seconds) shifting
        buffer for which any Representation is guaranteed to be available.
        This will go in the ‘timeShiftBufferDepth’ attribute of the ‘MPD’
        element. Default: 60.
    @minimum_update_period: (#int) Minimum update period (in seconds) of the
        manifest. This will go in the ‘minimumUpdatePeriod’ attribute of the
        ‘MPD’ element. Default: 0.

    """
    OPT = [
        Opt('f', 'format', value='webm_dash_manifest'),
        Opt('adaptation_sets'),
        EnableOpt('live'),
        IntOpt('chunk_start_index'),
        IntOpt('chunk_duration'),
        Opt('utc_timing_url'),
        IntOpt('time_shift_buffer_depth'),
        IntOpt('minimum_update_period'),
    ]


class WebMChunk(Container):
    """
    This muxer writes out WebM headers and chunks as separate files which can
    be consumed by clients that support WebM Live streams via DASH.


    ``WebM Live Chunk muxer options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @chunk_start_index: (#int) Index of the first chunk (defaults to 0).
    @audio_chunk_duration: (#int) Duration of each audio chunk in milliseconds
        (defaults to 5000).
    @header: (#str) Filename of the header where the initialization data will
        be written.
    """
    OPT = [
        Opt('f', 'format', value='webm_chunk'),
        IntOpt('chunk_start_index'),
        IntOpt('audio_chunk_duration'),
        Opt('header')
    ]
