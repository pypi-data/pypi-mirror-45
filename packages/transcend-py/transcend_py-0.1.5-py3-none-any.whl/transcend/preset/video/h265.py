from ...codec import H265, MotionEstimation, BFrames, Aac
from ...output import Video, Audio
from ...format import Mp4
from ..audio.aac import (
    LoFiAudio,
    MidFiAudio,
    HiFiAudio,
    LoFiHeAudio,
    MidFiHeAudio,
    HiFiHeAudio
)



class DefaultMe(MotionEstimation):
    def __init__(self, input=None, **opts):
        super(DefaultMe, self).__init__(
            me_method='umh',
            me_range=32,
            subq_est=10,
        )


class LowBFrames(BFrames):

    def __init__(self, input=None, **opts):
        super(LowBFrames, self).__init__(
            strategy=0,
            max=0,
        )


class DefaultBFrames(BFrames):

    def __init__(self, input=None, **opts):
        super(DefaultBFrames, self).__init__(
            strategy=2,
            max=3,
        )


class HighBFrames(BFrames):

    def __init__(self, input=None, **opts):
        super(HighBFrames, self).__init__(
            strategy=2,
            max=5,
        )

class BaseH265(Video):

    def __init__(self, input=None, **opts):
        super(BaseH265, self).__init__(
            DefaultMe(),
            pixel_format='yuv420p',
            codec=H265(rc_lookahead=60,
                       key_interval=120,
                       min_key_interval=1,
                       refs=4,
                       fast_pskip=True,
                       trellis=2,
                       psy_rd=(1.0, 1.0)),
            format=Mp4(),
            **opts)


class AnyDevice(BaseH265):

    def __init__(self, input=None, **opts):
        super(AnyDevice, self).__init__(
            LowBFrames(),
            audio=LoFiAudio,
            **opts)
        self.codec.set(size='424x240',
                       max_bitrate='576k',
                       buffer_size='864k',
                       profile='baseline',
                       level=2.1,
                       partitions=['p4x4'])


class AnyDevice360p(AnyDevice):

    def __init__(self, input=None, **opts):
        super(AnyDevice360p, self).__init__(
            LowBFrames(),
            **opts)
        self.codec.set(size='640x360',
                   level=3.0,
                   max_bitrate='896k',
                   buffer_size='1344k')


class Main360p(BaseH265):

    def __init__(self, input=None, **opts):
        super(Main360p, self).__init__(
            DefaultBFrames(),
            audio=LoFiHeAudio,
            **opts)
        self.codec.set(size='640x360',
                       max_bitrate='896k',
                       buffer_size='1344k',
                       profile='main',
                       level=3.1)


class High360p(Main360p):

    def __init__(self, input=None, **opts):
        super(High360p, self).__init__(**opts)
        self.codec.set(profile='high')


class Main480p(BaseH265):

    def __init__(self, input=None, **opts):
        super(Main480p, self).__init__(
            DefaultBFrames(),
            audio=MidFiHeAudio,
            **opts)
        self.codec.set(size='848x480',
                       max_bitrate='1536k',
                       buffer_size='2304k',
                       profile='main',
                       level=3.1)


class High480p(Main480p):

    def __init__(self, input=None, **opts):
        super(High480p, self).__init__(**opts)
        self.codec.set(profile='high')


class Main576p(BaseH265):
    def __init__(self, input=None, **opts):
        super(Main576p, self).__init__(
            DefaultBFrames(),
            audio=MidFiHeAudio,
            **opts)
        self.codec.set(size='960x576',
                       max_bitrate='2176k',
                       buffer_size='3264k',
                       profile='main',
                       level=3.1)


class High576p(Main576p):
    def __init__(self, input=None, **opts):
        super(High576p, self).__init__(**opts)
        self.codec.set(profile='high')


class High720p(BaseH265):
    def __init__(self, input=None, **opts):
        super(High720p, self).__init__(
            DefaultBFrames(),
            audio=HiFiHeAudio,
            **opts)
        self.codec.set(size='1280x270',
                       max_bitrate='2176k',
                       buffer_size='3264k',
                       profile='high',
                       level=4.0)


class High1080p(BaseH265):
    def __init__(self, input=None, **opts):
        super(High1080p, self).__init__(
            DefaultBFrames(),
            audio=HiFiHeAudio,
            **opts)
        self.codec.set(size='1920x1080',
                       max_bitrate='7552k',
                       buffer_size='11328k',
                       profile='high',
                       level=4.1)


class Super1080p(BaseH265):
    def __init__(self, input=None, **opts):
        super(Super1080p, self).__init__(
            HighBFrames(),
            audio=HiFiHeAudio,
            **opts)
        self.codec.set(size='1920x1080',
                       max_bitrate='12M',
                       buffer_size='18M',
                       profile='high',
                       level=4.1,
                       fast_pskip=False,
                       deblock_alpha=-2,
                       deblock_beta=-1)


class High1440p(BaseH265):
    def __init__(self, input=None, **opts):
        super(High1440p, self).__init__(
            HighBFrames(),
            audio=HiFiHeAudio,
            **opts)
        self.codec.set(size='2560x1440',
                       max_bitrate='18M',
                       buffer_size='30.48M',
                       profile='high',
                       level=4.1,
                       fast_pskip=False,
                       deblock_alpha=-2,
                       deblock_beta=-1)

High2k = High1440p


class High2160p(BaseH265):
    def __init__(self, input=None, **opts):
        super(High2160p, self).__init__(
            HighBFrames(),
            audio=HiFiHeAudio,
            **opts)
        self.codec.set(size='3840×2160',
                       max_bitrate='55M',
                       buffer_size='82.5M',
                       profile='high',
                       level=4.1,
                       fast_pskip=False,
                       deblock_alpha=-2,
                       deblock_beta=-1)

High4k = High2160p
