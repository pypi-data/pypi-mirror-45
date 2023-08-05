'''
AVC/H.264 Video Codec (Main or High profiles)
HE-AACv2 Audio Codec
Fragmented ISOBMFF Segments
MPEG-DASH “live” and “ondemand” profiles
Segments are IDR-aligned across Representations and have specific tolerances with regard to variation in segment durations.
CommonEncryption
SMPTE-TT Closed Captions


"urn:mpeg:dash:profile:isoff-live:2011". Supports ISOBMFF container, VOD and live streaming, using either the Segment Template: Time-Based or the Segment Template: Number-Based chunk addressing scheme.
"urn:mpeg:dash:profile:isoff-main:2011". Supports ISOBMFF container, VOD and live streaming, using the Segment List chunk addressing scheme.
'''
from ....codec import H264, Vpx, Vp9, MotionEstimation, BFrames, Aac, Opus
from ....output import Video, Audio
from ....format import Dash, Mp4
from .. import h264


#: DASH audio presets
#  MPEG-DASH spec specifically includes he-aac-v2 and multi-channel he-aac
LoFiDashAudio = Aac(bitrate='24k', sample_rate='44100', profile='aac_he_v2', channels=2)
MidFiDashAudio = Aac(bitrate='48k', sample_rate='44100', profile='aac_he_v2', channels=2)
HiFiDashAudio = Aac(bitrate='128k', sample_rate='44100', profile='aac_he_v2')


#: DASH recommended VPX settings
# http://wiki.webmproject.org/ffmpeg/vp9-encoding-guide
# http://wiki.webmproject.org/adaptive-streaming/instructions-to-playback-adaptive-webm-using-dash
# http://wiki.webmproject.org/zz-obsolete/instructions-to-playback-a-webm-dash-presentation

#: DASH
#  https://kvssoft.wordpress.com/2015/01/28/mpeg-dash-gop/
class BaseDashH264(h264.BaseH264):

    def _set_dash_opts(self):
        self.codec.key_interval(120)
        self.codec.flags('cgop')
        self.codec.min_key_interval(120)
        self.codec.scene_change_thresh(0)
        self.format = Mp4()
        self.format.movflags('frag_keyframe', 'faststart')
        self.format.merge(Dash())

        #if not self.format.min_seg_duration.val:
        #    self.format.min_seg_duration = 2

        self.format.single_file(True)
        self.audio = None
        self.disable_audio()
        self.disable_subtitles()


class H264xAnyDevice(h264.AnyDevice, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264xAnyDevice, self).__init__(*opt, **opts)
        self._set_dash_opts()


class H264xAnyDevice360p(h264.AnyDevice360p, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264xAnyDevice360p, self).__init__(*opt, **opts)
        self._set_dash_opts()


class H264x360p(h264.Main360p, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264x360p, self).__init__(*opt, **opts)
        self._set_dash_opts()


class H264x480p(h264.High480p, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264x480p, self).__init__(*opt, **opts)
        self._set_dash_opts()


class H264x576p(h264.High480p, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264x576p, self).__init__(*opt, **opts)
        self._set_dash_opts()


class H264x720p(h264.High720p, BaseDashH264):

    def __init__(self, *opt, **opts):
        super(H264x720p, self).__init__(*opt, **opts)
        self._set_dash_opts()


'''
FRAGMENTS

Live streams consist of fragments (self-contained units of frames which are not referencing any frame outside the fragment). A fragment always starts with a key-frame (intra-frame) therefore it is important that the encoder put in key frames regularly as this determines the size of the fragments.

The ideal fragment size is around 200 kBytes (or 1600 kbits). The key frame interval can be calculated with this formula:

1600k / <bitrate> * <framerate>
e.g. if you are publishing a 500 kbit stream with 16 fps, then: 1600 / 500 * 16 = 51.2 (or 1600000 / 500000 * 16 = 51.2) so every 52nd video frame should be a key frame.

The server splits fragments when it seems necessary. A soft minimum for frame size is currently 100k (no new fragment is started if a new key frame arrives within 100 kBytes from a previous key frame).

The hard maximum for a fragments is 2048 kBytes. This is twice the size needed to hold 2 seconds of a 4096 kbit/sec HD stream.
'''
