# -*- coding: utf-8 -*-
from ...cli import *
from .._container import *


__all__ = ('Segmenter',)


class Segmenter(Container):
    """
    This muxer outputs streams to a number of separate files of nearly fixed
    duration. Output filename pattern can be set in a fashion similar to image2,
    or by using a strftime template if the strftime option is enabled.

    |stream_segment| is a variant of the muxer used to write to streaming output
    formats, i.e. which do not require global headers, and is recommended for
    outputting e.g. to MPEG transport stream segments. |ssegment| is a shorter
    alias for |stream_segment|.

    Every segment starts with a keyframe of the selected reference stream,
    which is set through the |reference_stream| option.

    Note that if you want accurate splitting for a video file, you need to make
    the input key frames correspond to the exact splitting times expected by
    the segmenter, or the segment muxer will start the new segment with the key
    frame found next after the specified start time.

    The segment muxer works best with a single constant frame rate video.

    Optionally it can generate a list of the created segments, by setting the
    option segment_list. The list type is specified by the |segment_list_type|
    option. The entry filenames in the segment list are set by default to the
    basename of the corresponding segment files.


    ``Basic stream segmenter options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @incr_timecode (increment_tc): (#bool) If set to 1, increment timecode
        between each segment If this is selected, the input need to have a
        timecode in the first video stream. Default value is 0.
    @reference_stream: (#str) Set the reference stream, as specified by the
        string specifier. If specifier is set to auto, the reference is chosen
        automatically. Otherwise it must be a stream specifier (see the “Stream
        specifiers” chapter in the ffmpeg manual) which specifies the reference
        stream. The default value is auto.
    @inner_format (segment_format): (#str) Override the inner container format,
        by default it is guessed by the filename extension.
    @inner_format_opt (segment_format_options): (#dict) Set output format
        options using a :-separated list of key=value parameters. Values
        containing the : special character must be escaped.
    @list_file (segment_list): (#str) Generate also a listfile named name. If
        not specified no listfile is generated.
    @list_flags (segment_list_flags): (#tuple(flags)) Set flags affecting the
        segment list generation.
    @list_size (segment_list_size): (#int) Update the list file so that it
        contains at most size segments. If 0 the list file will contain all the
        segments. Default value is 0.
    @list_entry_prefix (segment_list_entry_prefix): (#str) Prepend prefix to
        each entry. Useful to generate absolute paths. By default no prefix is
        applied.
    @list_type (segment_list_type): (#str) Listing format: 'flat', 'csv, ext',
        'ffconcat', 'm3u8'
    @time (segment_time): (#int) Set segment duration to time, the value must
        be a duration specification. Default value is "2". See also the
        segment_times option.
    @at_clock_time (segment_atclocktime): (#bool) If set to "1" split at regular
        clock time intervals starting from 00:00 o’clock. The time value
        specified in segment_time is used for setting the length of the
        splitting interval.
    @clocktime_offset (segment_clocktime_offset): (#int) Delay the segment
        splitting times with the specified duration when using
        segment_atclocktime.
    @clocktime_wrap_duration (segment_clocktime_wrap_duration): (#float) Force
        the segmenter to only start a new segment if a packet reaches the muxer
        within the specified duration after the segmenting clock time. This way
        you can make the segmenter more resilient to backward local time jumps,
        such as leap seconds or transition to standard time from daylight
        savings time.
    @time_delta (segment_time_delta): (#float) Specify the accuracy time when
        selecting the start time for a segment, expressed as a duration
        specification. Default value is "0".
    @times (segment_times): (#tuple(#float)) Specify a list of split points.
        Times contains a list of comma separated duration specifications, in
        increasing order.
    @frames (segment_frames): (#tuple(#int)) Specify a list of split video
        frame numbers. frames contains a list of comma separated integer
        numbers, in increasing order.
    @wrap (segment_wrap): (#int) Wrap around segment index once it reaches
        limit.
    @start_number (segment_start_number): (#int) Set the sequence number of the
        first segment. Defaults to 0.
    @strftime: (#bool) Use the strftime function to define the name of the new
        segments to write. If this is selected, the output segment name must
        contain a strftime function template. Default value is 0.
    @break_non_keyframes: (#bool) If enabled, allow segments to start on
        frames other than keyframes. This improves behavior on some players
        when the time between keyframes is inconsistent, but may make things
        worse on others, and can cause some oddities during seeking.
        Defaults to 0.
    @reset_timestamps: (#bool) Reset timestamps at the begin of each segment,
        so that each segment will start with near-zero timestamps. It is meant
        to ease the playback of the generated segments. May not work with some
        combinations of muxers/codecs. It is set to 0 by default.
    @initial_offset: (#float) Specify timestamp offset to apply to the output
        packet timestamps. The argument must be a time duration specification,
        and defaults to 0.
    @write_empty (write_empty_segments): (#bool) If enabled, write an empty
        segment if there are no packets during the period a segment would
        usually span. Otherwise, the segment will be filled with the next
        packet written. Defaults to 0.
    """
    OPT = [
        Opt('f', 'format', value='segment'),
        EnableOpt('increment_tc', 'incr_timecode'),
        Opt('reference_stream'),
        Opt('segment_format', 'inner_format'),
        KeyValOpt('segment_format_options', 'inner_format_opt',
                  separator=':'),
        Opt('segment_list', 'list_file'),
        FlagsOpt('segment_list_flags', 'list_flags'),
        IntOpt('segment_list_size', 'list_size'),
        Opt('segment_list_entry_prefix', 'list_entry_prefix'),
        OneOfOpt('segment_list_type', 'list_type',
                 choices=('flat', 'csv, ext', 'ffconcat', 'm3u8')),
        FloatOpt('segment_time', 'time'),
        EnableOpt('segment_atclocktime', 'at_clock_time'),
        FloatOpt('segment_clocktime_offset', 'clocktime_offset'),
        FloatOpt('segment_clocktime_wrap_duration',
               'clocktime_wrap_duration'),
        FloatOpt('segment_time_delta', 'time_delta'),
        GroupOpt('segment_times', 'times', cast=float, separator=','),
        GroupOpt('segment_frames', 'frames', cast=int, separator=','),
        IntOpt('segment_wrap', 'wrap'),
        IntOpt('segment_start_number', 'start_number'),
        EnableOpt('strftime'),
        EnableOpt('break_non_keyframes'),
        EnableOpt('reset_timestamps'),
        FloatOpt('initial_offset'),
        EnableOpt('write_empty_segments', 'write_empty')
    ]
