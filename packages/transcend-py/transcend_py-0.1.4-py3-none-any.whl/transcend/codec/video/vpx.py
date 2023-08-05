# -*- coding: utf-8 -*-
"""
`VPX`
=====
https://trac.ffmpeg.org/wiki/Encode/VP8


Variable bitrates
~~~~~~~~~~~~~~~~~
- libvpx offers a variable bitrate mode by default. In this mode, it will
  simply try to reach the specified bit rate on average, e.g. 1 MBit/s.
  This is the "target bitrate".
- In addition to the "default" VBR mode, there's a constant quality mode
  (like in the x264 encoder) that will ensure that every frame gets the number
  of bits it deserves to achieve a certain quality level, rather than forcing
  the stream to have an average bit rate. This results in better overall
  quality and should be your method of choice when you encode video with
  libvpx. In this case, the target bitrate becomes the maximum allowed bitrate.
  You enable the constant quality mode with the CRF parameter.


Constant bitrates
~~~~~~~~~~~~~~~~~
Like most other encoders, libvpx offers a constant bitrate encoding mode as
well, which tries to encode the video in such a way that an average bitrate
is reached. This doesn't mean that every frame is encoded with the same amount
of bits (since it would harm quality), but the bitrate will be very constrained.
You should use constant bitrate encoding if you need your video files to have a
certain size, or if you're streaming the videos over a channel that only allows
a certain bit rate.
"""
from ...cli import *
from ...codec._codec import *


__all__ = 'Vpx', 'Vp8', 'Vp9',


class Vpx(VideoCodec):
    """
    VP8/VP9 format is supported through libvpx.

    To reduce the duplication of documentation, only the private options and
    some others requiring special attention are documented here. For the
    documentation of the undocumented generic options, see :class:VideoCodec.

    ``VPX-specific options``
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Source: http://wiki.webmproject.org/ffmpeg

    @undershoot_pct (undershoot-pct): (#int 0-100) Set datarate undershoot
        (min) percentage of the target bitrate.
    @overshoot_pct (overshoot-pct): (#int 0-100) Set datarate overshoot (max)
        percentage of the target bitrate.
    @crf: (#int 4-63) constant rate factor
    @tune: (#str) 'psnr' or 'ssim'
    @quality: (#str) 'best', 'good', 'realtime'
    @speed (cpu-used): (#int -16-16) Set quality/speed ratio modifier.
        Higher values speed up the encode at the cost of quality.
    @noise_sensitivity (nr): (#int 0-6) Crude temporal noise filter.
    @static_thresh (static-thresh): (#int) Set a change threshold on blocks
        below which they will be skipped by the encoder.
    @slices: Note that FFmpeg’s slices option gives the total number of
        partitions, while vpxenc’s token-parts is given as log2(partitions).
    @max_intra_rate (max-intra-rate): (#int) Set maximum I-frame bitrate as a
        percentage of the target bitrate. A value of 0 means unlimited.
    @force_key_frames: (#bool) VPX_EFLAG_FORCE_KF
    @auto_alt_ref (auto-alt-ref): (#int) Enable use of alternate reference
        frames (2-pass only). 0 for disabled, 1 for enabled.
    @arnr_max_frames (arnr-max-frames): (#int) Set altref noise reduction max
        frame count.
    @arnr_type (arnr-type): (#str) 'backward', 'forward', 'centered'
    @arnr_strength (arnr-strength): (#int 0-6) Set altref noise reduction filter
        strength.
    @error_resilient (error-resilient): (#int) Enable error resiliency features.
        0 for disabled, 1 for enabled.
    """
    OPT = [
        Opt('c:v', 'codec', value='libvpx'),
        BoundedOpt('undershoot-pct', 'undershoot_pct',
                   lower=0, upper=100),
        BoundedOpt('overshoot-pct', 'overshoot_pct',
                   lower=0, upper=100),
        BoundedOpt('crf', lower=4, upper=63),
        OneOfOpt('tune', choices=('psnr', 'ssim')),
        OneOfOpt('quality', choices=('best', 'good', 'realtime')),
        BoundedOpt('cpu-used', 'speed', lower=-16, upper=16),
        BoundedOpt('nr', 'noise_sensitivity', lower=0, upper=6),
        IntOpt('static-thresh', 'static_thresh'),
        OneOfOpt('slices', cast=int, choices=(1, 2, 4, 8)),
        BoundedOpt('max-intra-rate', 'max_intra_rate',
                   lower=0, upper=100),
        Flag('force_key_frames'),
        EnableOpt('auto-alt-ref', 'auto_alt_ref'),
        IntOpt('arnr-max-frames', 'arnr_max_frames'),
        OneOfOpt('arnr-type', 'arnr_type',
                 choices=('backward', 'forward', 'centered')),
        BoundedOpt('arnr-strength', 'arnr_strength', lower=0, upper=6),
        EnableOpt('error-resilient', 'error_resilient')
    ]


Vp8 = Vpx


class Vp9(Vp8):
    """
    ``VP9-specific options``
    ~~~~~~~~~~~~~~~~~~~~~~~~
    @dash: (#int) Set MPEG-DASH segment duration.
    @lossless: (#bool) Enable lossless mode. 1 for enabled, 0 for disabled
    @tile_columns (tile-columns): (#int) Set number of tile columns to use.
        Note this is given as log2(tile_columns). For example, 8 tile columns
        would be requested by setting the tile-columns option to 3.
    @tile_rows (tile-rows): (#int) Set number of tile rows to use. Note this
        is given as log2(tile_rows). For example, 4 tile rows would be
        requested by setting the tile-rows option to 2.
    @frame_parallel (frame-parallel): (#bool) Enable frame parallel
        decodability features. 1 for enabled, 0 for disabled.
    @aq_mode (aq-mode): (#int 0-3) Set adaptive quantization mode
        (0: off (default), 1: variance 2: complexity, 3: cyclic refresh).
    @colorspace: (#str) 'rgb', 'bt709', 'unspecified', 'bt470bg', 'smpte170m',
        'smpte240m', 'bt2020_ncl'
    """
    OPT = Vpx.OPT + [
        Opt('c:v', 'codec', value='libvpx-vp9'),
        IntOpt('dash'),
        OneOfOpt('strict', choices=('very', 'strict', 'normal',
                                    'experimental'),
                           value='experimental'),
        IntOpt('tile-columns', 'tile_columns'),
        IntOpt('tile-rows', 'tile_rows'),
        EnableOpt('frame-parallel', 'frame_parallel'),
        BoundedOpt('aq-mode', 'aq_mode', lower=0, upper=3),
        OneOfOpt('colorspace',
                 choices=('rgb', 'bt709', 'unspecified', 'bt470bg',
                          'smpte170m', 'smpte240m', 'bt2020_ncl'))
    ]
