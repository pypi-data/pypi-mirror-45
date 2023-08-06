# -*- coding: utf-8 -*-
"""
`AAC`
============
libfdk_aac wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = 'Aac',


class Aac(AudioCodec):
    """
    The libfdk-aac library is based on the Fraunhofer FDK AAC code from the
    Android project. This encoder is considered to produce output on par or
    worse at 128kbps to the the native FFmpeg AAC encoder but can often produce
    better sounding audio at identical or lower bitrates and has support for
    the AAC-HE profiles.

    VBR encoding, enabled through the vbr or flags +qscale options, is
    experimental and only works with some combinations of parameters.


    ``Advanced Audio Coding (AAC) encoder``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @profile: (#str) Set audio profile: 'aac_low', 'aac_he', 'aac_he_v2',
        'aac_ld', 'aac_eld'. If not specified it is set to ‘aac_low’.
    @afterburner: (#bool) Enable afterburner feature if set to 1, disabled if
        set to 0. This improves the quality but also the required processing
        power.
    @eld_sbr: (#bool) Enable SBR (Spectral Band Replication) for ELD if set to
        1, disabled if set to 0. Default value is 0.
    @signaling: (#str) Set SBR/PS signaling style: 'default', 'implicit',
        'explicit_sbr', 'explicit_hierarchical'
    @latm: (#bool) Output LATM/LOAS encapsulated data if set to 1, disabled if
        set to 0.
    @header_period: (#int) Set StreamMuxConfig and PCE repetition period
        (in frames) for sending in-band configuration buffers within LATM/LOAS
        transport layer.
    @vbr: (#int 1-5) Set VBR mode, from 1 to 5. 1 is lowest quality (though
        still pretty good) and 5 is highest quality. A value of 0 will disable
        VBR, and CBR (Constant Bit Rate) is enabled. Currently only the
        ‘aac_low’ profile supports VBR encoding.
    @flags: (#str) '+qscale' Enable fixed quality, VBR (Variable Bit Rate)
        mode. Note that VBR is implicitly enabled when the vbr value is
        positive.
    """
    OPT = [
        Opt('c:a', 'codec', value='aac'),
        OneOfOpt(
            'profile:a',
            'profile',
            choices=('aac_low', 'aac_he', 'aac_he_v2', 'aac_ld')
        ),
        FlagsOpt('flags'),
        EnableOpt('afterburner'),
        EnableOpt('eld_sbr'),
        OneOfOpt(
            'signaling',
            choices=(
                'default',
                'implicit',
                'explicit_sbr',
                'explicit_hierarchical'
            )
        ),
        EnableOpt('latm'),
        IntOpt('header_period'),
        BoundedOpt('vbr', lower=1, upper=5)
    ]
