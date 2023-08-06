from ...codec import H264, MotionEstimation, BFrames, Aac, Quantizer
from ...output import Video, Audio
from ...format import Mp4
from ...utils import calc_scale
from ..audio.aac import LoFiAudio, MidFiAudio, HiFiAudio


class DefaultMe(MotionEstimation):
    def __init__(self, input=None, **opts):
        super(DefaultMe, self).__init__(
            me_method='umh',
            me_range=32,
            subq_est=10,
        )


class LowQuantizer(Quantizer):
    def __init__(self, input=None, **opts):
        super(LowQuantizer, self).__init__(
            min=3,
            curve_compression=0.9
        )


class DefaultQuantizer(Quantizer):
    def __init__(self, input=None, **opts):
        super(DefaultQuantizer, self).__init__(
            curve_compression=0.9
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
            strategy=1,
            max=16,
        )


class HighBFrames(BFrames):

    def __init__(self, input=None, **opts):
        super(HighBFrames, self).__init__(
            strategy=2,
            max=3,
        )


class BaseH264(Video):

    def __init__(self, *opt, **opts):
        super().__init__(
            DefaultMe(),
            DefaultQuantizer(),
            *opt,
            pixel_format='yuv420p',
            codec=H264(
                # key_interval=120,
                # min_key_interval=1,
                frame_rate=30,
                fast_pskip=True,
                scene_change_thresh=40,
            ),
            format=Mp4(),
            **opts
        )
        # self.format.movflags('faststart')

        if self.output is not None and self.codec.size.val is not None:
            self.output.filters.set(scale=calc_scale(self.codec.size.val))


class AnyDevice(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            LowBFrames(),
            LowQuantizer(),
            audio=LoFiAudio,
            **opts
        )
        self.codec.set(
            size='424x240',
            max_bitrate='576k',
            buffer_size='864k',
            frame_rate=24,
            profile='baseline',
            level=3,
            partitions=['p4x4'],
            trellis=0
        )


class AnyDevice360p(AnyDevice):
    def __init__(self, input=None, **opts):
        super().__init__(**opts)
        self.codec.set(size='640x360',
                       level=3,
                       frame_rate=30,
                       max_bitrate='1024k',
                       buffer_size='1536k')


class Main360p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            DefaultBFrames(),
            audio=LoFiAudio,
            **opts)
        self.codec.set(
            size='640x360',
            max_bitrate='1024k',
            buffer_size='1536k',
            profile='main',
            level=3.1,
            coder=1,
            trellis=2
        )


class High360p(Main360p):
    def __init__(self, input=None, **opts):
        super().__init__(**opts)
        self.codec.set(profile='high')


class Main480p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            DefaultBFrames(),
            audio=MidFiAudio,
            **opts)
        self.codec.set(
            size='848x480',
            max_bitrate='1536k',
            buffer_size='2304k',
            profile='main',
            level=3.1,
            coder=1,
            trellis=2,
            rc_lookahead=32
        )


class High480p(Main480p):
    def __init__(self, input=None, **opts):
        super().__init__(**opts)
        self.codec.set(profile='high')


class Main576p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            DefaultBFrames(),
            audio=MidFiAudio,
            **opts)
        self.codec.set(
            size='960x576',
            max_bitrate='2176k',
            buffer_size='3264k',
            profile='main',
            level=3.1,
            coder=1,
            trellis=2,
            rc_lookahead=40
        )


class High576p(Main576p):
    def __init__(self, input=None, **opts):
        super().__init__(**opts)
        self.codec.set(profile='high')


class High720p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            DefaultBFrames(),
            audio=HiFiAudio,
            **opts)
        self.codec.set(
            size='1280x720',
            max_bitrate='5242k',
            buffer_size='7863k',
            profile='high',
            level=4,
            coder=1,
            trellis=2,
            rc_lookahead=60
        )


class High1080p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            DefaultBFrames(),
            audio=HiFiAudio,
            **opts
        )
        self.codec.set(
            size='1920x1080',
            max_bitrate='7552k',
            buffer_size='11328k',
            frame_rate=60,
            profile='high',
            level=4.1,
            coder=1,
            trellis=2,
            rc_lookahead=60
        )


class Super1080p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            HighBFrames(),
            audio=HiFiAudio,
            **opts)
        self.codec.set(
            size='1920x1080',
            max_bitrate='12M',
            buffer_size='18M',
            frame_rate=60,
            profile='high',
            level=4.1,
            fast_pskip=False,
            deblock_alpha=-2,
            deblock_beta=-1,
            coder=1,
            trellis=2,
            rc_lookahead=120
        )


class High1440p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            HighBFrames(),
            audio=HiFiAudio,
            **opts)
        self.codec.set(
            size='2560x1440',
            max_bitrate='18M',
            buffer_size='30.48M',
            frame_rate=60,
            profile='high',
            level=4.1,
            fast_pskip=False,
            deblock_alpha=-2,
            deblock_beta=-1,
            coder=1,
            trellis=2,
            rc_lookahead=175
        )

High2k = High1440p


class High2160p(BaseH264):
    def __init__(self, input=None, **opts):
        super().__init__(
            HighBFrames(),
            audio=HiFiAudio,
            **opts)
        self.codec.set(
            size='3840×2160',
            max_bitrate='55M',
            buffer_size='82.5M',
            frame_rate=60,
            profile='high',
            level=4.1,
            fast_pskip=False,
            deblock_alpha=-2,
            deblock_beta=-1,
            coder=1,
            trellis=2,
            rc_lookahead=175
        )

High4k = High2160p
