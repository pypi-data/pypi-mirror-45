# -*- coding: utf-8 -*-
from pathlib import Path
from ..cli import *
from ._protocol import Protocol


__all__ = 'FileIn', 'FileOut',


class _File(Protocol):
    OPT = [EnableOpt('truncate'), ByteOpt('blocksize')]


class FileIn(_File):
    def __init__(self, filename, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'filename', value=filename),
            **opts
        )


class FileOut(_File):
    def __init__(self, filename, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'filename', value=filename),
            **opts
        )

        try:
            self.path = Path(filename)
            self.path.parent.mkdir(0o744, parents=True)
        except FileExistsError:
            pass
