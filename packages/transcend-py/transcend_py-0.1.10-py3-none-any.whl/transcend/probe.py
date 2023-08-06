# -*- coding: utf-8 -*-
"""
`FFProbe Wrapper`
~~~~~~~~~~~~~~~~~
>>> import transcend as ts
>>> probe = ts.Probe('https://s3.amazonaws.com/bucket/vid.mp4')
>>> probe.exe()
..
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
| (Executing)                                                                  |
| ffprobe                                                                      |
|··············································································|
|(Output) ffprobe version git-2016-06-13-1f87233 Copyright (c) 2007-2016 the FF|
|  built with gcc 4.8 (Ubuntu 4.8.4-2ubuntu1~14.04.3)                          |
|  configuration: --enable-gpl --enable-gnutls --enable-openssl --enable-nonfre|
|  libavutil      55. 24.100 / 55. 24.100                                      |
|  libavcodec     57. 46.100 / 57. 46.100                                      |
|  libavformat    57. 38.100 / 57. 38.100                                      |
|  libavdevice    57.  0.101 / 57.  0.101                                      |
|  libavfilter     6. 46.101 /  6. 46.101                                      |
|  libswscale      4.  1.100 /  4.  1.100                                      |
|  libswresample   2.  1.100 /  2.  1.100                                      |
|  libpostproc    54.  0.100 / 54.  0.100                                      |
|Input #0, mov,mp4,m4a,3gp,3g2,mj2, from 'https://s3.amazonaws.com/bucket/vid.m|
|  Metadata:                                                                   |
|    major_brand     : isom                                                    |
|    minor_version   : 512                                                     |
|    compatible_brands: isomiso2avc1mp41                                       |
|    encoder         : Lavf57.25.100                                           |
|  Duration: 00:00:01.60, start: 0.000000, bitrate: 478 kb/s                   |
|    Stream #0:0(und): Audio: aac (LC) (mp4a / 0x6134706D), 32000 Hz, stereo, f|
|    Metadata:                                                                 |
|      handler_name    : SoundHandler                                          |
|    Stream #0:1(und): Video: h264 (Constrained Baseline) (avc1 / 0x31637661), |
|    Metadata:                                                                 |
|      handler_name    : VideoHandler                                          |
|                                                                              |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
..

"""
import os
import sys
import subprocess

from .cli import *
from .ffmpeg import Ffmpeg


# TODO: https://trac.ffmpeg.org/wiki/FFprobeTips


class Probe(Ffmpeg):
    """
    ``FFProbe wrapper``
    ~~~~~~~~~~~~~~~~~~~
    @format: (#str) Force format to use
    @unit: (#bool) Show the unit of the displayed values.
    @prefix: (#bool) Use SI prefixes for the displayed values.
    @byte_binary_prefix: (#bool) Force the use of binary prefixes for byte
        values.
    @sexagesimal: (#bool) Use sexagesimal format HH:MM:SS.MICROSECONDS for time
        values.
    @pretty: (#bool) Prettify the format of the displayed values, it
        corresponds to the options "-unit -prefix -byte_binary_prefix
        -sexagesimal".
    @print_format: (#str) Set the output printing format
    @sections: (#bool) Print sections structure and section information,
        and exit. The output is not meant to be parsed by a machine.
    @select_streams: (#str) Select only the streams specified by
        |stream_specifier|. This option affects only the options related to
        streams (e.g. show_streams, show_packets, etc.)
    @show_data_hash: (#str) Show a hash of payload data, for packets with
        |-show_packets| and for codec extradata with |-show_streams|
    @show_error: (#bool) Show information about the error found when trying to
        probe the input.
    @show_format: (#bool) Show information about the container format of the
        input multimedia stream.
    @show_packets: (#bool) Show information about each packet contained in the
        input multimedia stream.
    @show_frames: (#bool) Show information about each frame and subtitle
        contained in the input multimedia stream.
    @show_streams: (#bool) Show information about each media stream contained
        in the input multimedia stream.
    @show_chapters: (#bool) Show information about chapters stored in the
        format.
    @count_frames: (#bool) Count the number of frames per stream and report it
        in the corresponding stream section.
    @count_packets: (#bool) Count the number of packets per stream and report
        it in the corresponding stream section.
    @read_interval: (#str) Read only the specified intervals. |read_interval|
        must be a sequence of interval specifications separated by ",".
        ffprobe will seek to the interval starting point, and will continue
        reading from that.
    @private: (#bool) Prevents showing private data
    @show_program_version: (#bool) Show information related to program version.
    @show_library_versions: (#bool) Show information related to library
        versions.
    @show_versions: (#bool) Show information related to program and library
        versions. This is the equivalent of setting both -show_program_version
        and -show_library_versions options.
    @show_pixel_formats: (#bool) Show information about all pixel formats
        supported by FFmpeg.
    @bitexact: (#bool) Force bitexact output, useful to produce output which
        is not dependent on the specific build.
    @show_entries: (#dict) e.g. |{'stream': 'avg_frame_rate,height,width'}|
    """
    __slots__ = Ffmpeg.__slots__

    OPT = Ffmpeg.OPT + [
        Opt('f', 'format'),
        Flag('unit'),
        Flag('prefix'),
        Flag('byte_binary_prefix'),
        Flag('sexagesimal'),
        Flag('pretty'),
        Opt('print_format', value='json'),
        Flag('sections'),
        Opt('select_streams'),
        Opt('show_data_hash'),
        Flag('show_error'),
        Flag('show_format'),
        Opt('show_format_entry'),
        Flag('show_packets'),
        Flag('show_frames'),
        Flag('show_streams'),
        Flag('show_chapters'),
        Flag('count_frames'),
        Flag('count_packets'),
        GroupOpt('read_interval', separator=','),
        Flag('private'),
        Flag('show_program_version'),
        Flag('show_library_versions'),
        Flag('show_versions'),
        Flag('show_pixel_formats'),
        KeyValOpt('show_entries', separator=':'),
        Flag('bitexact')
    ]

    def __init__(self, *a, bin=None, **kw):
        bin = bin or os.path.join(os.path.expanduser('~'), 'bin/ffprobe')
        super(Probe, self).__init__(*a, bin=bin, **kw)

    # #
    # REMEMBER
    # ~~~~~~~~
    # ffprobe test_files/test/foo/1080.m4s -print_format json -show_entries stream -show_data_hash sha512
    # ffmpeg -i test_files/test/foo/360.m4s -f hash -hash sha512 -
    # #
    def _exec_pipe(self, *outputs, stdout=None, stderr=None):
        return super(Probe, self)._exec_pipe(
            *outputs,
            stdout=stdout,
            stderr=stderr,
            no_faststart=True
        )

    def is_playable(self, criteria=None):
        """ Tests if the file is considered playable based on given criteria
            compared against the JSON results of the FFPROBE command
        """
        #: TODO
        pass




'''
import json
from vital.debug import Timer
import transcend as ts
t = Timer()
t.start()
f = ts.Probe(show_format=True, show_streams=True)
f.input = ts.protocol.FileIn('test_files/test.vpx.webm')
# f.input = ts.protocol.S3In('s3://xfaps.queue/v/56/56294846-3904-45e1-b2af-c071cfbb629b.MOV')
# f.input = ts.protocol.S3In('s3://xfaps.queue/Sintel.2010.1080p.mkv')
# f.input = ts.protocol.S3In('s3://xfaps.queue/v/42/42e2bc9c-eb23-44b7-b870-1aba196b1172.mp4')
output = f.run()
print(json.dumps(json.loads(output.stdout.decode()), indent=2))
print(t.stop())
'''
