import os
import math
from ....codec import H264, Vpx, Vp9, MotionEstimation, BFrames,\
                                   Aac, Opus
from ....output import Video, Audio
from ....format import Hls, Mp4
from .. import h264
# from transcend.coding.utils import calc_gop


def calc_gop(frame_rate, hls_time=3):
    # https://github.com/vbence/stream-m#fragments
    return frame_rate * hls_time


#: HLS audio presets
AnyHlsAudio = Aac(bitrate='64k', sample_rate='44100', channels=2)
LoFiHlsAudio = Aac(bitrate='96k', sample_rate='44100', channels=2)
MidFiHlsAudio = Aac(bitrate='160k', sample_rate='44100', channels=2)
HiFiHlsAudio = Aac(bitrate='256k', sample_rate='44100', channels=6)


class BaseHlsAacAudio(Audio):
    def set_hls_opts(self):
        # FRAG SIZE
        # https://github.com/vbence/stream-m#fragments
        if not hasattr(self.format, 'hls_flags'):
            self.format.merge(Hls())

        self.format.movflags('frag_keyframe', 'empty_moov')
        # self.format.movflags('empty_moov')
        # self.format.hls_flags('single_file', 'append_list', 'round_durations')
        self.format.hls_flags('append_list')
        self.format.playlist_type('vod')
        self.format.allow_cache(True)
        self.format.list_size(0)

        bitrate = self.codec.bitrate.val or\
                  self.codec.max_bitrate.val or\
                  self.codec.min_bitrate.val

        if not self.format.time.val:
            self.format.time(3)

        try:
            fn, fe = os.path.splitext(self.output.path.name)
            op = self.output.path.parent.joinpath(fn)
            self.format.init_filename(f'{op.parts[-1]}/init.m4a')
            # self.format.init_filename(op.joinpath('init.m4a'))
            self.format.segment_filename(op.joinpath('%d.m4s'))
            op.mkdir(mode=0o777, parents=True, exist_ok=True)
        except AttributeError:
            pass

        if not self.format.segment_type.val:
            self.format.segment_type('fmp4')

        self.disable_video()
        self.disable_subtitles()


class AacxAnyDevice(BaseHlsAacAudio):

    def __init__(self, *opt, **opts):
        super().__init__(
            *opt,
            codec=AnyHlsAudio,
            format=Mp4(),
            **opts
        )
        self.set_hls_opts()


class AacxLoFi(BaseHlsAacAudio):

    def __init__(self, *opt, **opts):
        super().__init__(
            *opt,
            codec=LoFiHlsAudio,
            format=Mp4(),
            **opts
        )
        self.set_hls_opts()


class AacxMidFi(BaseHlsAacAudio):

    def __init__(self, *opt, **opts):
        super().__init__(
            *opt,
            codec=MidFiHlsAudio,
            format=Mp4(),
            **opts
        )
        self.set_hls_opts()


class AacxHiFi(BaseHlsAacAudio):

    def __init__(self, *opt, **opts):
        super().__init__(
            *opt,
            codec=HiFiHlsAudio,
            format=Mp4(),
            **opts
        )
        self.set_hls_opts()


#: Hls
#  https://kvssoft.wordpress.com/2015/01/28/mpeg-dash-gop/
class BaseHlsH264(h264.BaseH264):

    def set_hls_opts(self):
        self.codec.scene_change_thresh(0)
        self.format.movflags('frag_keyframe', 'empty_moov')
        self.format.movflags('empty_moov')

        if not hasattr(self.format, 'hls_flags'):
            self.format.merge(Hls())

        # FRAG SIZE
        # https://github.com/vbence/stream-m#fragments
        if not self.format.time.val:
            self.format.time(3)

        key_int = calc_gop(self.codec.frame_rate.val or 30, self.format.time.val)

        # if self.codec.max_bitrate.val and not self.codec.bitrate.val:
        #     self.codec.bitrate(self.codec.max_bitrate.val)
        self.codec.key_interval(key_int)
        self.codec.flags('cgop')
        self.codec.min_key_interval(key_int)

        self.format.list_size(0)
        # self.format.hls_flags('single_file', 'append_list', 'round_durations')
        self.format.hls_flags('append_list')
        self.format.playlist_type('vod')
        self.format.allow_cache(True)
        try:
            fn, fe = os.path.splitext(self.output.path.name)
            op = self.output.path.parent.joinpath(fn)
            self.format.init_filename(f'{op.parts[-1]}/init.m4v')
            # self.format.init_filename(op.joinpath('init.m4v'))
            self.format.segment_filename(op.joinpath('%d.m4s'))
            op.mkdir(mode=0o777, parents=True, exist_ok=True)
        except AttributeError:
            pass

        if not self.format.segment_type.val:
            self.format.segment_type('fmp4')

        self.audio = None
        self.disable_audio()
        self.disable_subtitles()


class H264xAnyDevice(h264.AnyDevice, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.codec.set(
            profile='main',
            level=3.1,
            trellis=2
        )
        self.set_hls_opts()


class H264xAnyDevice360p(h264.AnyDevice360p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


class H264x360p(h264.Main360p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


class H264x480p(h264.High480p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


class H264x576p(h264.High576p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


class H264x720p(h264.High720p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


class H264x1080p(h264.High1080p, BaseHlsH264):

    def __init__(self, *opt, **opts):
        super().__init__(*opt, **opts)
        self.set_hls_opts()


'''
FRAGMENTS

Live streams consist of fragments (self-contained units of frames which are not referencing any frame outside the fragment). A fragment always starts with a key-frame (intra-frame) therefore it is important that the encoder put in key frames regularly as this determines the size of the fragments.

The ideal fragment size is around 200 kBytes (or 1600 kbits). The key frame interval can be calculated with this formula:

1600k / <bitrate> * <framerate>
e.g. if you are publishing a 500 kbit stream with 16 fps, then: 1600 / 500 * 16 = 51.2 (or 1600000 / 500000 * 16 = 51.2) so every 52nd video frame should be a key frame.

The server splits fragments when it seems necessary. A soft minimum for frame size is currently 100k (no new fragment is started if a new key frame arrives within 100 kBytes from a previous key frame).

The hard maximum for a fragments is 2048 kBytes. This is twice the size needed to hold 2 seconds of a 4096 kbit/sec HD stream.
'''
