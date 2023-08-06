# -*- coding: utf-8 -*-
from ...cli import *
from .._container import *


__all__ = 'Hls',


# https://ffmpeg.org/ffmpeg-formats.html#hls-2


class Hls(Container):
    """
    Apple HTTP Live Streaming muxer that segments MPEG-TS according to the
    HTTP Live Streaming (HLS) specification.

    It creates a playlist file, and one or more segment files. The output
    filename specifies the playlist filename.

    By default, the muxer creates a file for each segment produced. These files
    have the same name as the playlist, followed by a sequential number and a
    .ts extension.


    ``HLS muxer options``
    ~~~~~~~~~~~~~~~~~~~~~
    @time (hls_time): (#float) Set the segment length in seconds. Default value
        is 2.
    @list_size (hls_list_size): (#int) Update the list file so that it contains
        at most size segments. If 0 the list file will contain all the segments.
        Default value is 0.
    @wrap (hls_wrap): (#int) Wrap around segment index once it reaches
        limit.
    @ts_options (hls_ts_options): (#dict) Set output format options.
    @start_number: (#int) Set the sequence number of the
        first segment. Defaults to 0.
    @allow_cache (hls_allow_cache): (#bool) Explicitly set whether the client
        MAY (1) or MUST NOT (0) cache media segments.
    @base_url (hls_base_url): (#str) Append baseurl to every entry in the
        playlist. Useful to generate playlists with absolute paths.
    @segment_filename (hls_segment_filename): (#str) Set the segment filename.
        Unless hls_flags single_file is set filename is used as a string format
        with the segment number:
    @use_localtime_mkdir: (#bool) Used together with -use_localtime, it will
        create up to one subdirectory which is expanded in filename.
    @key_info_file (hls_key_info_file): (#str) Use the information in
        key_info_file for segment encryption. The first line of key_info_file
        specifies the key URI written to the playlist. The key URL is used to
        access the encryption key during playback. The second line specifies
        the path to the key file used to obtain the key during the encryption
        process. The key file is read as a single packed array of 16 octets in
        binary format. The optional third line specifies the initialization
        vector (IV) as a hexadecimal string to be used instead of the segment
        sequence number (default) for encryption. Changes to key_info_file will
        result in segment encryption with the new key/IV and an entry in the
        playlist for the new key URI/IV.
    @hls_flags: (flags)
    @playlist_type (hls_playlist_type): (#str) 'vod' or 'event'
    @init_filename: (#str) set filename to the fragment files header file,
        default filename is init.mp4.
    """
    OPT = [
        Opt('f', 'format', value='hls'),
        FloatOpt('hls_time', 'time'),
        IntOpt('hls_list_size', 'list_size'),
        KeyValOpt('hls_ts_options', 'ts_options'),
        IntOpt('start_number'),
        OneOfOpt(
            'hls_start_number_source',
            'start_number_source',
            choices=('generic', 'epoch', 'datetime')
        ),
        EnableOpt('hls_allow_cache', 'allow_cache'),
        Opt('hls_base_url', 'base_url'),
        Opt('hls_segment_filename', 'segment_filename'),
        Flag('use_localtime'),
        Flag('use_localtime_mkdir'),
        Opt('hls_key_info_file', 'key_info_file'),
        FlagsOpt('hls_flags'),
        OneOfOpt(
            'hls_playlist_type',
            'playlist_type',
            choices=('vod', 'event')
        ),
        EnableOpt('hls_enc', 'encrypt'),
        Opt('hls_enc_key', 'encrypt_key'),
        Opt('hls_enc_key_url', 'encrypt_key_url'),
        Opt('hls_enc_iv', 'encrypt_iv'),
        OneOfOpt(
            'hls_segment_type',
            'segment_type',
            choices=('fmp4', 'mpegts')
        ),
        Opt('hls_fmp4_init_filename', 'init_filename'),
        OneOfOpt('method', ('PUT', 'GET', 'POST', 'DELETE', 'HEAD')),
        Opt('user_agent')
    ]
