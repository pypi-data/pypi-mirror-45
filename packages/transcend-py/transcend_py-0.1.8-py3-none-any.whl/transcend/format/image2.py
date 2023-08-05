# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'Image2',


class Image2(Container):
    """
    The image file muxer writes video frames to image files.

    The output filenames are specified by a pattern, which can be used to
    produce sequentially numbered series of files. The pattern may contain the
    string "%d" or "%0Nd", this string specifies the position of the characters
    representing a numbering in the filenames. If the form "%0Nd" is used, the
    string representing the number in each filename is 0-padded to N digits.
    The literal character ’%’ can be specified in the pattern with the
    string "%%".

    If the pattern contains "%d" or "%0Nd", the first filename of the file
    list specified will contain the number 1, all the following numbers will
    be sequential.

    The pattern may contain a suffix which is used to automatically determine
    the format of the image files to write.

    For example the pattern "img-%03d.bmp" will specify a sequence of filenames
    of the form img-001.bmp, img-002.bmp, ..., img-010.bmp, etc. The pattern
    "img%%-%d.jpg" will specify a sequence of filenames of the form img%-1.jpg,
    img%-2.jpg, ..., img%-10.jpg, etc.


    `Image2 container format`
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    @start_number: (#int) Start the sequence from the specified number. Default
        value is 0.
    @update: (#bool) If set to 1, the filename will always be interpreted as
        just a filename, not a pattern, and the corresponding file will be
        continuously overwritten with new images. Default value is 0.
    @strftime: (#bool) If set to 1, expand the filename with date and time
        information from strftime(). Default value is 0.
    """
    OPT = [
        Opt('f', 'format', value='image2'),
        IntOpt('start_number'),
        EnableOpt('update'),
        EnableOpt('strftime')
    ]
