# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Matroska', 'WebM',


class Matroska(Container):
    """
    `Matroska (mkv) container format`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @reserve_index_space: (#int) By default, this muxer writes the index for
        seeking (called cues in Matroska terms) at the end of the file,
        because it cannot know in advance how much space to leave for the
        index at the beginning of the file. However for some use cases – e.g.
        streaming where seeking is possible but slow – it is useful to put the
        index at the beginning of the file.
    """
    OPT = [
        Opt('f', 'format', value='mkv'),
        IntOpt('reserve_index_space')
    ]


class WebM(Matroska):
    OPT = [Opt('f', 'format', value='webm')]
