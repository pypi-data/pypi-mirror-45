# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'HlsHttpIn', 'HlsFileIn',


class HlsHttpIn(Protocol):
    """
    `HTTP Live Streaming protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Read Apple HTTP Live Streaming compliant segmented stream as a uniform one.
    The M3U8 playlists describing the segments can be remote HTTP resources or
    local files, accessed using the standard file protocol. The nested protocol
    is declared by specifying "+proto" after the hls URI scheme name, where
    proto is either "file" or "http".

    |hls+http://host/path/to/remote/resource.m3u8|
    |hls+file://path/to/local/resource.m3u8|
    """
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value='hls+http://' + endpoint),
            **opts
        )

class HlsFileIn(HlsHttpIn):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value='hls+http://' + endpoint),
            **opts
        )
