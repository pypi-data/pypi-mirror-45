from multiprocessing import cpu_count
from ...codec import Theora
from ...output import Video, Audio
from ...format import WebM
from ..audio import vorbis



class BaseTheora(Video):

    def __init__(self, input=None, **opts):
        super(BaseTheora, self).__init__(
            pixel_format='yuv420p',
            codec=Theora(threads=cpu_count()),
            format=WebM(),
            **opts)


class AnyDevice(BaseTheora):

    def __init__(self, input=None, **opts):
        super(AnyDevice, self).__init__(
            audio=vorbis.LoFiAudio,
            **opts)
        self.codec.set(size='424x240',
                       bitrate='576k',
                       max_bitrate='576k',
                       buffer_size='864k')


class AnyDevice360p(AnyDevice):

    def __init__(self, input=None, **opts):
        super(AnyDevice360p, self).__init__(
            **opts)
        self.codec.set(size='640x360',
                       bitrate='896k',
                       max_bitrate='896k',
                       buffer_size='1344k')


class Theora360p(BaseTheora):

    def __init__(self, input=None, **opts):
        super(Theora360p, self).__init__(
            audio=vorbis.LoFiAudio,
            **opts)
        self.codec.set(size='640x360',
                       bitrate='896k',
                       max_bitrate='896k',
                       buffer_size='1344k',
                       crf=16)


class Theora480p(BaseTheora):

    def __init__(self, input=None, **opts):
        super(Theora480p, self).__init__(
            audio=vorbis.MidFiAudio,
            **opts)
        self.codec.set(size='848x480',
                       bitrate='1536k',
                       max_bitrate='1536k',
                       buffer_size='2304k')


class Theora576p(BaseTheora):
    def __init__(self, input=None, **opts):
        super(Theora576p, self).__init__(
            audio=vorbis.MidFiAudio,
            **opts)
        self.codec.set(size='960x576',
                       bitrate='2176k',
                       max_bitrate='2176k',
                       buffer_size='3264k')


class Theora720p(BaseTheora):
    def __init__(self, input=None, **opts):
        super(Theora720p, self).__init__(
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='1280x270',
                       bitrate='2176k',
                       max_bitrate='2176k',
                       buffer_size='3264k')


class Theora1080p(BaseTheora):
    def __init__(self, input=None, **opts):
        super(Theora1080p, self).__init__(
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='1920x1080',
                       bitrate='7552k',
                       max_bitrate='7552k',
                       buffer_size='11328k')


class Theora1440p(BaseTheora):
    def __init__(self, input=None, **opts):
        super(Theora1440p, self).__init__(
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='2560x1440',
                       bitrate='18M',
                       max_bitrate='18M',
                       buffer_size='30.48M')

Theora2k = Theora1440p


class Theora2160p(BaseTheora):
    def __init__(self, input=None, **opts):
        super(Theora2160p, self).__init__(
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='3840×2160',
                       bitrate='55M',
                       max_bitrate='55M',
                       buffer_size='82.5M')

Theora4k = Theora2160p
