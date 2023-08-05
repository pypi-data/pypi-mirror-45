from multiprocessing import cpu_count
from ...codec import Vpx, Vp9, Quantizer
from ...output import Video, Audio
from ...format import WebM
from ..audio import opus, vorbis


class BaseVpx(Video):
    def __init__(self, input=None, **opts):
        super(BaseVpx, self).__init__(
            Quantizer(min=4, max=63),
            pixel_format='yuv420p',
            codec=Vpx(threads=cpu_count(),
                      crf=10),
            format=format.WebM(),
            **opts)


class BaseVp9(Video):
    def __init__(self, input=None, **opts):
        super(BaseVp9, self).__init__(
            Quantizer(min=4, max=63),
            pixel_format='yuv420p',
            codec=Vpx(threads=cpu_count(),
                      key_interval=120,
                      crf=10),
            format=WebM(),
            **opts)


class AnyDevice(BaseVpx):

    def __init__(self, input=None, **opts):
        super(AnyDevice, self).__init__(
            audio=vorbis.LoFiAudio,
            **opts)
        self.codec.set(size='424x240',
                       bitrate='712k',
                       max_bitrate='712k',
                       buffer_size='1068k',
                       quality='realtime',
                       speed=9,
                       crf=12)


class AnyDevice360p(AnyDevice):

    def __init__(self, input=None, **opts):
        super(AnyDevice360p, self).__init__(
            **opts)
        self.codec.set(size='640x360',
                       bitrate='712k',
                       max_bitrate='712k',
                       buffer_size='1068k',
                       quality='realtime',
                       speed=9,
                       crf=12)


class Vpx360p(BaseVpx):

    def __init__(self, input=None, **opts):
        super(Vpx360p, self).__init__(
            audio=vorbis.LoFiAudio,
            **opts)
        self.codec.set(size='640x360',
                       bitrate='1024k',
                       max_bitrate='1024k',
                       buffer_size='1536k',
                       quality='good',
                       speed=9)


class Vpx480p(BaseVpx):

    def __init__(self, input=None, **opts):
        super(Vpx480p, self).__init__(
            audio=vorbis.MidFiAudio,
            **opts)
        self.codec.set(size='848x480',
                       bitrate='1896k',
                       max_bitrate='1896k',
                       buffer_size='2844k',
                       quality='good',
                       speed=6)


class Vpx576p(BaseVpx):
    def __init__(self, input=None, **opts):
        super(Vpx576p, self).__init__(
            audio=vorbis.MidFiAudio,
            **opts)
        self.codec.set(size='960x576',
                       bitrate='2176k',
                       max_bitrate='2176k',
                       buffer_size='3264k',
                       quality='good',
                       speed=6)


class Vpx720p(BaseVpx):
    def __init__(self, input=None, **opts):
        super(Vpx720p, self).__init__(
            Quantizer(min=0, max=50),
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='1280x270',
                       bitrate='2576k',
                       max_bitrate='2576k',
                       buffer_size='3864k',
                       quality='good')


class Vpx1080p(BaseVpx):
    def __init__(self, input=None, **opts):
        super(Vpx1080p, self).__init__(
            Quantizer(min=0, max=50),
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='1920x1080',
                       bitrate='7552k',
                       max_bitrate='7552k',
                       buffer_size='11328k',
                       crf=8,
                       quality='good')


class Vpx1440p(BaseVpx):
    def __init__(self, input=None, **opts):
        super(Vpx1440p, self).__init__(
            Quantizer(min=0, max=40),
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='2560x1440',
                       bitrate='18M',
                       max_bitrate='18M',
                       buffer_size='30.48M',
                       crf=6,
                       quality='best')


Vpx2k = Vpx1440p


class Vpx2160p(BaseVpx):
    def __init__(self, input=None, **opts):
        super(Vpx2160p, self).__init__(
            Quantizer(min=0, max=40),
            audio=vorbis.HiFiAudio,
            **opts)
        self.codec.set(size='3840×2160',
                       bitrate='55M',
                       max_bitrate='55M',
                       buffer_size='82.5M',
                       crf=4,
                       quality='best')


Vpx4k = Vpx2160p


class Vp9240p(BaseVp9):

    def __init__(self, input=None, **opts):
        super(Vp9360p, self).__init__(
            audio=opus.LoFiAudio,
            **opts)
        self.codec.set(size='424x240',
                       bitrate='576k',
                       max_bitrate='576k',
                       buffer_size='864k',
                       crf=16,
                       quality='realtime',
                       speed=9)


class Vp9360p(BaseVp9):

    def __init__(self, input=None, **opts):
        super(Vp9360p, self).__init__(
            audio=opus.LoFiAudio,
            **opts)
        self.codec.set(size='640x360',
                       bitrate='896k',
                       max_bitrate='896k',
                       buffer_size='1344k',
                       crf=16,
                       quality='realtime',
                       speed=9)


class Vp9480p(BaseVp9):

    def __init__(self, input=None, **opts):
        super(Vp9480p, self).__init__(
            audio=opus.MidFiAudio,
            **opts)
        self.codec.set(size='848x480',
                       bitrate='1536k',
                       max_bitrate='1536k',
                       buffer_size='2304k',
                       crf=16,
                       quality='good',
                       speed=6)


class Vp9576p(BaseVp9):
    def __init__(self, input=None, **opts):
        super(Vp9576p, self).__init__(
            audio=opus.MidFiAudio,
            **opts)
        self.codec.set(size='960x576',
                       bitrate='2176k',
                       max_bitrate='2176k',
                       buffer_size='3264k',
                       crf=12,
                       quality='good',
                       speed=6)


class Vp9720p(BaseVp9):
    def __init__(self, input=None, **opts):
        super(Vp9720p, self).__init__(
            Quantizer(min=0, max=50),
            audio=opus.HiFiAudio,
            **opts)
        self.codec.set(size='1280x270',
                       bitrate='2576k',
                       max_bitrate='2576k',
                       buffer_size='3864k',
                       quality='good')


class Vp91080p(BaseVp9):
    def __init__(self, input=None, **opts):
        super(Vp91080p, self).__init__(
            Quantizer(min=0, max=50),
            audio=opus.HiFiAudio,
            **opts)
        self.codec.set(size='1920x1080',
                       bitrate='7552k',
                       max_bitrate='7552k',
                       buffer_size='11328k',
                       crf=8,
                       quality='good')


class Vp91440p(BaseVp9):
    def __init__(self, input=None, **opts):
        super(Vp91440p, self).__init__(
            Quantizer(min=0, max=40),
            audio=opus.HiFiAudio,
            **opts)
        self.codec.set(size='2560x1440',
                       bitrate='18M',
                       max_bitrate='18M',
                       buffer_size='30.48M',
                       crf=6,
                       quality='best')


Vp92k = Vp91440p


class Vp92160p(BaseVp9):
    def __init__(self, input=None, **opts):
        super(Vp92160p, self).__init__(
            Quantizer(min=0, max=40),
            audio=opus.HiFiAudio,
            **opts)
        self.codec.set(size='3840×2160',
                       bitrate='55M',
                       max_bitrate='55M',
                       buffer_size='82.5M',
                       crf=4,
                       quality='best')


Vp94k = Vp92160p
