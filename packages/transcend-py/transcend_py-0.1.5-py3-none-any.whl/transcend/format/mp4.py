# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Mp4',


class Mp4(Container):
    """
    The mov/mp4/ismv muxer supports fragmentation. Normally, a MOV/MP4 file has
    all the metadata about all packets stored in one location (written at the
    end of the file, it can be moved to the start for better playback by adding
    faststart to the movflags, or using the qt-faststart tool). A fragmented
    file consists of a number of fragments, where packets and metadata about
    these packets are stored together. Writing a fragmented file has the a
    dvantage that the file is decodable even if the writing is interrupted
    (while a normal MOV/MP4 is undecodable if it is not properly finished),
    and it requires less memory when writing very long files (since writing
    normal MOV/MP4 files stores info about every single packet in memory until
    the file is closed). The downside is that it is less compatible with other
    applications.


    `Mp4 container format`
    ~~~~~~~~~~~~~~~~~~~~~~
    @moov_size: (#str) Reserves space for the moov atom at the beginning of the
        file instead of placing the moov atom at the end. If the space reserved
        is insufficient, muxing will fail.
    @frag_duration: (#int) Create fragments that are duration microseconds long.
    @frag_size: (#str) Create fragments that contain up to size bytes of
        payload data.
    @min_frag_duration: (#int) Don’t create fragments that are shorter than
        duration microseconds long.
    """
    OPT = [
        Opt('f', 'format', value='mp4'),
        ByteOpt('moov_size'),
        # FlagsOpt('movflags', value='+faststart'),
        FlagsOpt('movflags'),
        IntOpt('frag_duration'),
        ByteOpt('frag_size'),
        IntOpt('min_frag_duration')
    ]
