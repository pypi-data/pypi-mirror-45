from ..output import Video
from ..codec import VideoCodec
from ..protocol import FileOut


class Thumbnails(Video):
    def __init__(self, *opt, filename='%d.jpg', fps=1, **opts):
        super().__init__(
            *opt,
            codec=VideoCodec(),
            output=FileOut(filename),
            filters={'fps': fps},
            **opts
        )
