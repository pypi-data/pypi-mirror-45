# -*- coding: utf-8 -*-
from .cli import *
from .format import Container
from .probe import Probe


__all__ = 'Output', 'Video', 'Audio', 'Subtitle'


DEFAULT_OUTPUT_OPT = [
    Opt('map_metadata'),
    FloatOpt('t', 'duration'),
    TimeOpt('to', 'stop_time'),
    TimeOpt('ss', 'start_time'),
    TimeOpt('sseof', 'rstart_time'),
    Opt('target'),
    KeyValOpt('program'),
    KeyValOpt('metadata'),
    IntOpt('frames'),
    Opt('filter_script'),
    Opt('reinit_filter'),
    ByteOpt('fs', 'max_size'),
    Flag('seek_timestamp'),
    Flag('apad', 'audio_pad'),
    Flag('discard'),
    Flag('disposition')
]


class Output(OptSet):
    '''
    -map_metadata       set metadata information of outfile from infile
    -t duration         record or transcode "duration" seconds of audio/video
    -to time_stop       record or transcode stop time
    -fs limit_size      set the limit file size in bytes
    -ss time_off        set the start time offset
    -sseof time_off     set the start time offset relative to EOF
    -seek_timestamp     enable/disable seeking by timestamp with -ss
    -metadata string=string  add metadata (key=value)
    -program title=string:st=number...  add program with specified streams
    -target type        specify target file type
    -apad               audio pad
    -frames number      set the number of frames to output
    -filter_script filename  read stream filtergraph description from a file
    -reinit_filter      reinit filtergraph on input parameter changes
    -discard            discard
    -disposition        disposition
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        """ @codec: (:class:transcend.coding.codecs.Codec) codec settings
            @format: (:class:transcend.coding.format.Container)
                format settings
            @output: (#str or :class:transcend.coding.protocols.Protocol)
                output protocol
        """
        self.codec = None
        self.format = None
        self.output = None

        if len(opts):
            for prop in ('codec', 'format', 'output'):
                try:
                    val = opts[prop]
                    del opts[prop]
                    setattr(self, prop, val)
                except KeyError:
                    pass

        super().__init__(*(list(opt) + DEFAULT_OUTPUT_OPT + self.OPT))
        self.set(**opts)

    @property
    def live_opts(self):
        if self.codec is not None:
            for cmd in self.codec.live_opts:
                yield cmd
        if self.format is not None:
            for cmd in self.format.live_opts:
                yield cmd
        for cmd in super(Output, self).live_opts:
            yield cmd
        if self.output is not None:
            if isinstance(self.output, str):
                yield self.output
            else:
                for cmd in self.output.live_opts:
                    yield cmd

    def save_to(self, output):
        self.output = output


class Video(Output):
    '''
    -vframes number     set the number of video frames to output
    -vn                 disable video
    -an                 disable audio
    -vcodec codec       force video codec ('copy' to copy stream)
    -timecode hh:mm:ss[:;.]ff  set initial TimeCode value.
    -pass n             select the pass number (1 to 3)
    -vf filter_graph    set video filters
    -dn                 disable data
    -pix_fmt            set pixel format
    '''
    OPT = [
        BoundedOpt('pass', 'pass_n', lower=1, upper=2),
        IntOpt('vframes', 'frames'),
        Opt('vcodec'),
        Flag('vn', 'disable'),
        Flag('an', 'disable_audio'),
        TimeOpt('timecode', 'timecode'),
        KeyValOpt('filter:v', 'filters'),
        KeyValOpt('filter_complex', 'complex_filters'),
        Flag('dn', 'disable_data'),
        Flag('sn', 'disable_subtitles'),
        Opt('pix_fmt', 'pixel_format')
    ]

    def __init__(self, *opt, **opts):
        """ @audio: (:class:Audio) audio track settings
            @codec: (:class:transcend.coding.codecs.Codec) codec settings
            @format: (:class:transcend.coding.format.Container)
                format settings
            @output: (#str or :class:transcend.coding.protocols.Protocol)
                output protocol
        """
        self.audio = None
        self.subtitles = None

        if len(opts):
            for prop in ('audio', 'subtitles'):
                try:
                    val = opts[prop]
                    del opts[prop]
                except KeyError:
                    val = None
                setattr(self, prop, val)
        super().__init__(*opt, **opts)

    def set_audio(self, audio):
        self.audio = audio

    @property
    def live_opts(self):
        if self.audio is not None:
            for cmd in self.audio.live_opts:
                yield cmd
        if self.subtitles is not None:
            for cmd in self.subtitles.live_opts:
                yield cmd
        for cmd in super(Video, self).live_opts:
            yield cmd

    def resize(self):
        '''https://trac.ffmpeg.org/wiki/Scaling%20(resizing)%20with%20ffmpeg'''


class Audio(Output):
    '''
    -aframes number     set the number of audio frames to output
    -an                 disable audio
    -vn                 disable video
    -acodec codec       force audio codec ('copy' to copy stream)
    -af filter_graph    set audio filters
    '''
    OPT = [
        IntOpt('aframes', 'frames'),
        Opt('acodec'),
        Flag('an', 'disable'),
        Flag('vn', 'disable_video'),
        Flag('sn', 'disable_subtitles'),
        KeyValOpt('filter:a', 'filters')
    ]


class Subtitle(Output):
    '''
    -s size             set frame size (WxH or abbreviation)
    -sn                 disable subtitle
    -scodec codec       force subtitle codec ('copy' to copy stream)
    -stag fourcc/tag    force subtitle tag/fourcc
    -fix_sub_duration   fix subtitles duration
    -canvas_size size   set canvas size (WxH or abbreviation)
    -spre preset        set the subtitle options to the indicated preset
    '''
    OPT = [
        SizeOpt('s', 'size'),
        Flag('sn', 'disable'),
        Flag('vn', 'disable_video'),
        Flag('an', 'disable_audio'),
        Opt('c:s', 'codec'),
        Opt('stag', 'tag'),
        Flag('fix_duration'),
        SizeOpt('canvas_size'),
        Opt('spre', 'preset')
    ]
