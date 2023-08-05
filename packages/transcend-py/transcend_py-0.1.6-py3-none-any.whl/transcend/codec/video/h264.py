# -*- coding: utf-8 -*-
"""
`H.264`
=======

``iOS Compatability``
|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
| Profile     Level      Devices                                               |
|––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
| Baseline    3.0   All devices                                                |
|                    -profile:v baseline -level 3.0                            |
| Baseline    3.1   iPhone 3G and later, iPod touch 2nd generation and later   |
|                    -profile:v baseline -level 3.1                            |
| Main        3.1   iPad (all versions), Apple TV 2 and later, iPhone 4 and    |
|                   later                                                      |
|                    -profile:v main -level 3.1                                |
| Main        4.0   Apple TV 3 and later, iPad 2 and later, iPhone 4s and later|
|                    -profile:v main -level 4.0                                |
| High        4.0   Apple TV 3 and later, iPad 2 and later, iPhone 4s and later|
|                    -profile:v high -level 4.0                                |
| High        4.1   iPad 2 and later, iPhone 4s and later, iPhone 5c and later |
|                    -profile:v high -level 4.1                                |
| High        4.2   iPad Air and later, iPhone 5s and later                    |
|                    -profile:v high -level 4.2                                |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
Source: https://trac.ffmpeg.org/wiki/Encode/H.264


Presets
~~~~~~~
Preset determines how fast the encoding process will be – at the expense of
compression efficiency. Put differently, if you choose ultrafast, the encoding
process is going to run fast, but the file size will be larger when compared to
medium. The visual quality will be the same. Valid presets are ultrafast,
superfast, veryfast, faster, fast, medium, slow, slower, veryslow and placebo.


Encoding for dumb players
~~~~~~~~~~~~~~~~~~~~~~~~~
You may need to use |-pix_fmt yuv420p| for your output to work in QuickTime and
most other players. These players only supports the YUV planar color space with
4:2:0 chroma subsampling for H.264 video. Otherwise, depending on your source,
ffmpeg may output to a pixel format that may be incompatible with these
players.


Encoding for web
~~~~~~~~~~~~~~~~
|-movflags +faststart| (Container-level)

"""
from ...cli import *
from .._codec import *


__all__ = 'H264',


class H264(VideoCodec):
    """
    libx264 supports an impressive number of features, including 8x8 and 4x4
    adaptive spatial transform, adaptive B-frame placement, CAVLC/CABAC entropy
    coding, interlacing (MBAFF), lossless mode, psy optimizations for detail
    retention (adaptive quantization, psy-RD, psy-trellis).

    Many libx264 encoder options are mapped to FFmpeg global codec options,
    while unique encoder options are provided through private options.
    Additionally the x264opts and x264-params private options allows one to
    pass a list of key=value tuples as accepted by the libx264 x264_param_parse
    function.

    To reduce the duplication of documentation, only the private options and
    some others requiring special attention are documented here. For the
    documentation of the undocumented generic options, see :class:VideoCodec.

    |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|
    | Levels          Max Bitrates            Max Resolutions                  |
    |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
    | Level     Baseline/Main    High      Resolution@Max Frame Rate           |
    |––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––|
    | 1             64            80           176×144@15.0                    |
    | 1.1           192           240          352×288@7.5                     |
    | 2             2,000         2,500        352×288@30.0                    |
    | 2.1           4,000         5,000        352×576@25.0                    |
    | 3             10,000        12,500       720×576@25.0                    |
    | 3.1           14,000        17,500       1,280×720@30.0                  |
    | 3.2           20,000        25,000       1,280×1,024@42.2                |
    | 4             20,000        25,000       2,048×1,024@30.0                |
    | 4.1           50,000        62,500       2,048×1,024@30.0                |
    | 4.2           50,000        62,500       2,048×1,080@60.0                |
    | 5             135,000       168,750      3,672×1,536@26.7                |
    | 5.1           240,000       300,000      4,096×2,304@26.7                |
    | 5.2           240,000       300,000      4,096×2,304@56.3                |
    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

    ``H.264-specific options``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    @profile: (#str) Set profile restrictions.
    @fast_firstpass (fastfirstpass): (#bool) Enable fast settings when encoding
        first pass, when set to 1. When set to 0, it has the same effect of
        x264’s --slow-firstpass option.
    @preset: (#str) Preset determines how fast the encoding process will be –
        at the expense of compression efficiency. Valid presets are ultrafast,
        superfast, veryfast, faster, fast, medium, slow, slower, veryslow and
        placebo.
    @crf: (#int) Set the quality for constant quality mode.
    @crf_max: (#int) In CRF mode, prevents VBV from lowering quality beyond
        this point.
    @qp: (#int) Set constant quantization rate control method parameter.
    @aq_mode (aq-mode): (#str) Set AQ method.
    @aq_strength (aq-strength): (#float) Set AQ strength, reduce blocking and
        blurring in flat and textured areas.
    @psy: (#int) Use psychovisual optimizations when set to 1. When set to 0,
        it has the same effect as x264’s --no-psy option.
    @psy_rd (psy-rd): (#tuple(#float)) Set strength of psychovisual
        optimization, in psy-rd:psy-trellis format.
    @rc_lookahead (rc-lookahead): (#int) Set number of frames to look ahead for
        frametype and ratecontrol.
    @weightb: (#int) Enable weighted prediction for B-frames when set to 1.
        When set to 0, it has the same effect as x264’s --no-weightb option.
    @weightp: (#str) Set weighted prediction method for P-frames.
    @ssim: (#bool) Enable calculation and printing SSIM stats after the
        encoding.
    @intra_refresh (intra-refresh): (#int) Enable the use of Periodic Intra
        Refresh instead of IDR frames when set to 1.
    @avcintra_class (avcintra-class): (#int) Configure the encoder to generate
        AVC-Intra. Valid values are 50, 100 and 200.
    @bluray_compat (bluray-compat): (#bool) Configure the encoder to be
        compatible with the bluray standard. It is a shorthand for setting
        "bluray-compat=1 force-cfr=1".
    @b_bias (b-bias): (#int) Set the influence on how often B-frames are used.
    @b_pyramid (b-pyramid): (#str) Set method for keeping of some B-frames as
        references.
    @mixed_refs (mixed-refs): (#int) Enable the use of one reference per
        partition, as opposed to one reference per macroblock when set to
        1. When set to 0, it has the same effect as x264’s --no-mixed-refs
        option.
    @8x8dct: (#int) Enable adaptive spatial transform (high profile 8x8
        transform) when set to 1. When set to 0, it has the same effect as
        x264’s --no-8x8dct option.
    @fast_pskip (fast-pskip): (#int) Enable early SKIP detection on
        P-frames when set to 1. When set to 0, it has the same effect as
        x264’s --no-fast-pskip option.
    @aud: (#int) Enable use of access unit delimiters when set to 1.
    @mbtree: (#int) Enable use macroblock tree ratecontrol when set to 1.
        When set to 0, it has the same effect as x264’s --no-mbtree option.
    @cplxblur: (#float) Set fluctuations reduction in QP (before curve
        compression).
    @partitions: (#tuple(#str)) e.g. ('parti4x4', 'partp8x8') or ('all',)
        Set partitions to consider as a comma-separated list of.
    @direct_prediction (direct-pred): (#str) Set direct MV prediction mode.
    @slice_max_size (slice-max-size): (#str) Set the limit of the size of each
        slice in bytes. If not specified but RTP payload size (ps) is specified,
        that is used.
    @nal_hrd (nal-hrd): (#str) Set signal HRD information (requires vbv-bufsize
        to be set).
    @x264opts: (#dict(key=value)) Set any x264 option, see x264 --fullhelp for
        a list.
    @deblock_beta: (#int)
    @deblock_alpha: (#int) One of H.264's main features is the in-loop
        deblocker, which avoids the problem of blocking artifacts disrupting
        motion estimation. This requires a small amount of decoding CPU, but
        considerably increases quality in nearly all cases. Its strength may
        be raised or lowered in order to avoid more artifacts or keep more
        detail, respectively. Deblock has two parameters: alpha (strength) and
        beta (threshold). Recommended defaults:-deblockalpha 0 -deblockbeta 0
        (Must have '-flags +loop')
    """
    OPT = [
        Opt('c:v', 'codec', value='libx264'),
        OneOfOpt('profile:v', 'profile',
                  choices=('baseline', 'extended', 'main', 'high')),
        OneOfOpt(
            'level',
            cast=str,
            choices=(
                '1', '1b', '1.1', '1.2', '1.3', '2', '2.1', '3', '3.1', '3.2',
                '4', '4.1', '4.2', '5', '5.1', '5.2', '6', '6.1', '6.2'
            )
        ),
        OneOfOpt('preset', cast=str,
                 choices=('ultrafast', 'superfast', 'veryfast',
                          'faster', 'fast', 'medium', 'slow', 'slower',
                          'veryslow', 'placebo')),
        BoundedOpt('crf', lower=0, upper=51),
        BoundedOpt('crf_max', lower=0, upper=51),
        BoundedOpt('qp', lower=0, upper=51),
        OneOfOpt('aq-mode', 'aq_mode',
                 choices=('none', 'variance', 'autovariance')),
        FloatOpt('aq-strength', 'aq_strength'),
        EnableOpt('psy'),
        GroupOpt('psy-rd', 'psy_rd', cast=float, separator=':'),
        IntOpt('rc-lookahead', 'rc_lookahead'),
        EnableOpt('coder'),
        EnableOpt('fastfirstpass', 'fast_firstpass'),
        EnableOpt('weightb'),
        OneOfOpt('weightp', choices=('none', 'simple', 'smart')),
        Flag('ssim'),
        EnableOpt('mixed-refs', 'mixed_refs'),
        EnableOpt('8x8dct'),
        EnableOpt('fast-pskip', 'fast_pskip'),
        EnableOpt('aud'),
        EnableOpt('mbtree'),
        FloatOpt('cplxblur'),
        EnableOpt('intra-refresh', 'intra_refresh'),
        OneOfOpt('avcintra-class', 'avcintra_class', cast=int,
                 choices=(50, 100, 200)),
        GroupOpt('partitions', separator=','),
        Flag('bluray-compat', 'bluray_compat'),
        ByteOpt('slice-max-size', 'slice_max_size'),
        OneOfOpt('b-pyramid', 'b_pyramid',
                 choices=('none', 'strict', 'normal')),
        OneOfOpt('thread_type', choices=('slice', 'frame')),
        OneOfOpt('nal-hrd', 'nal_hrd', choices=('none', 'vbr', 'cbr')),

        OneOfOpt('direct-pred', 'direct_prediction',
                 choices=('none', 'spatial', 'temporal', 'auto')),
        KeyValOpt('x264opts', separator=':'),
        Opt('tune'),
        IntOpt('deblockalpha', 'deblock_alpha'),
        IntOpt('deblockbeta', 'deblock_beta')
    ]


# nvenc_h264
# -pixel_format yuv444p
# https://trac.ffmpeg.org/wiki/HWAccelIntro
