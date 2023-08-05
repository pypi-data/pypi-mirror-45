# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = ('Aiff',)


class Aiff(Container):
    """
    ``Audio Interchange File Format container format``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @write_id3v2: (#bool) Enable ID3v2 tags writing when set to 1.
        Default is 0 (disabled).
    @id3v2_version: (#int) Select ID3v2 version to write. Currently only
        version 3 and 4 (aka. ID3v2.3 and ID3v2.4) are supported. The default
        is version 4.

    """
    OPT = [
        Opt('f', 'format', value='aiff'),
        EnableOpt('write_id3v2'),
        OneOfOpt('id3v2_version', cast=int, choices=(3, 4))
    ]
