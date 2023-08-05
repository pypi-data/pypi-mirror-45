# -*- coding: utf-8 -*-
from ..cli import *


__all__ = 'Container',


DEFAULT_OPT = [
    FlagsOpt('avioflags', 'flags'),
    IntOpt('probesize', 'probe_size'),
    IntOpt('packetsize', 'packet_size'),
    FlagsOpt('fflags'),
    EnableOpt('seek2any', 'seek_to_any'),
    IntOpt('analyzeduration', 'analyze_duration'),
    Opt('cryptokey', 'crypto_key'),
    IntOpt('indexmem', 'index_memory'),
    IntOpt('rtbufsize', 'rt_bufsize'),
    FlagsOpt('fdebug'),
    IntOpt('max_delay'),
    IntOpt('fpsprobesize', 'fps_probesize'),
    IntOpt('audio_prelaod'),
    IntOpt('chunk_duration'),
    ByteOpt('chunk_size'),
    FlagsOpt('err_detect'),
    IntOpt('max_interleave_delta'),
    EnableOpt('use_wallclock_as_timestamps'),
    OneOfOpt('avoid_negative_ts',
             choices=('make_non_negative', 'make_zero', 'auto',
                      'disabled')),
    EnableOpt('skip_initial_bytes'),
    EnableOpt('correct_ts_overflow'),
    EnableOpt('flush_packets'),
    TimeOpt('output_ts_offset'),
    Opt('dump_separator')
]


class Container(OptSet):
    """
    `Container format options`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    @avioflags: (flags)
    @probe_size (probesize): (#int) Set probing size in bytes, i.e. the size of
        the data to analyze to get stream information. A higher value will
        enable detecting more information in case it is dispersed into the
        stream, but will increase latency. Must be an integer not lesser than
        32. It is 5000000 by default.
    @packet_size (packetsize): (#int) Set packet size.
    @fflags: (flags) Set format flags.
    @seek_to_any (seek2any): (#bool) Allow seeking to non-keyframes on demuxer
        level when supported if set to 1. Default is 0.
    @analyze_duration (analyzeduration): (#int) Specify how many microseconds
        are analyzed to probe the input. A higher value will enable detecting
        more accurate information, but will increase latency. It defaults to
        5,000,000 microseconds = 5 seconds.
    @crypto_key (cryptokey): (#str) Set decryption key.
    @index_memory (indexmem): (#int) Set max memory used for timestamp index
        (per stream).
    @rt_bufsize (rtbufsize): (#int) Set max memory used for buffering real-time
        frames.
    @fdebug: (flags) Print specific debug info.
    @max_delay: (#int) Set maximum muxing or demuxing delay in microseconds.
    @fps_probesize (fpsprobesize): (#int) Set number of frames used to
        probe fps.
    @audio_preload: (#int) Set microseconds by which audio packets should be
        interleaved earlier.
    @chunk_duration: (#int) Set microseconds for each chunk.
    @chunk_size: (#int) Set size in bytes for each chunk.
    @err_detect: (flags) Set error detection flags. f_err_detect is deprecated
        and should be used only via the ffmpeg tool.
    @max_interleave_delta: (#int) Set maximum buffering duration for
        interleaving. The duration is expressed in microseconds, and defaults
        to 1000000 (1 second).
    @use_wallclock_as_timestamps: (#bool) Use wallclock as timestamps if set
        to 1. Default is 0.
    @avoid_negative_ts: (#str) 'make_non_negative', 'make_zero', 'auto',
        'disabled'
    @skip_initial_bytes: (#bool) Set number of bytes to skip before reading
        header and frames if set to 1. Default is 0.
    @correct_ts_overflow: (#bool) Correct single timestamp overflows if set
        to 1. Default is 1.
    @flush_packets: (#bool) Flush the underlying I/O stream after each packet.
        Default 1 enables it, and has the effect of reducing the latency; 0
        disables it and may slightly increase performance in some cases.
    @output_ts_offset: (#str (time)) Set the output time offset. Offset must be
        a time duration specification, see the Time duration section in the
        ffmpeg-utils(1) manual.
    @dump_separator: (#str) Separator used to separate the fields printed on
        the command line about the Stream parameters.
    """
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_OPT + self.OPT + list(opt)), **opts)

    def __call__(self, *args, **kwargs):
        return self.__class__(*args, **kwargs)
