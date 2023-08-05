# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = ('Aac',)


class Aac(Container):
    """
    ``AAC container format` `
    """
    OPT = [FlagsOpt('movflags', value='+faststart')]
