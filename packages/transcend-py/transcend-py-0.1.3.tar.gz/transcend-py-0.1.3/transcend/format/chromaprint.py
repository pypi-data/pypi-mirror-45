# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Chromaprint',


class Chromaprint(Container):
    """
    This muxer feeds audio data to the Chromaprint library, which generates a
    fingerprint for the provided audio data. It takes a single signed
    native-endian 16-bit raw audio stream.


    ``Chromaprint container format``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @silence_threshold: (#int -1-32767) Threshold for detecting silence, ranges
        from 0 to 32767. -1 for default (required for use with the AcoustID
        service).
    @algorithm: (#int) Algorithm index to fingerprint with.
    @fp_format: (#str) Format to output the fingerprint as: 'raw', 'compressed',
        'base64'
    """
    OPT = [
        Opt('f', 'format', value='chromaprint'),
        BoundedOpt('silence_threshold', lower=-1, upper=32767),
        OneOfOpt('fp_format', choices=('raw', 'compressed', 'base64'))
    ]
