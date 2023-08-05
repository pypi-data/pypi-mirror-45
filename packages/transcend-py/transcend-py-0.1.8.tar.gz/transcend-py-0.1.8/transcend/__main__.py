# -*- coding: utf-8 -*-
'''
                #####
                 ##
                 #
    `Transcend` #
    ~~~~~~~~~~~~~~~~~
    High performance video and audio transcoding for aliens.


    usage: ts s3://queue.bucket:v/big-buck-bunny.mp4 \
              s3://public.bucket:v/big-buck-bunny.mp4 \
              --budget 0.35 \
              --max-filesize 150M


    python usage:

    import transcend as ts
    audio_track = ts.Audio(codec=ts.Aac(), channels=2)
    output = ts.Video(codec=ts.H264(profile='high',
                                    level=4.1,
                                    size=(1280, 720)),
                      container=ts.format.Mp4(),
                      audio=audio_track)

    Things to remember
    ==================

    * bitrate = file size / duration
        * allow setting desired or max file size
        * 24 MBPS * (2 hours * 60 minutes / hour * 60 seconds / minute) = 172,800 MB
        ------------------------
        frames per sec. - 30
        res.width - 1920
        res.height - 1080
        Gop size - 12
        frame/sec by Gopsize  (30/12=2,5)
        pixels in 1 frame  (1920*1080=2.073.600)
        pixels in frame/sec  (2.073.600*30=62.208.000)
        bitrate max needed  (62.208.000/2,5=24.883.200) -24000 - 24Mb/s
        bitrate with 70% loses  (24.883.200/0,7=17.418.240) - 17000 - 17Mb/s
        For 720i with loses 70% and will give a size of file equalling 10Gb
        for losses of 40% give 4Gb and screens with a res of 720-480 and an
        aspect ratio of 3/4, this will give size 3,7Gb for 70% and
        1,4Gb for 40%
    * audio bitrate
        * fileSize = (bitsPerSample * samplesPerSecond * channels * duration) / 8;
            * 30 seconds of stereo will take up (8 * 44100 * 2 * 30) / 8 = 2,646,000
    * optimize for -> encoding speed OR best compression


    Cheat sheet
    ===========
    http://www.labnol.org/internet/useful-ffmpeg-commands/28490/
    http://www.catswhocode.com/blog/19-ffmpeg-commands-for-all-needs
    https://blogs.dropbox.com/tech/2014/02/video-processing-at-dropbox/
    http://www.lighterra.com/papers/videoencodingh264/
'''

from .output import Audio, Video
from .ffmpeg import Ffmpeg
from . import codec, format, preset, protocol


class Transcend(object):

    def from_json(self):
        pass

    def from_dict(self):
        pass

    def from_namedtuple(self):
        pass


if __name__ == '__main__':
    from vital.debug import Timer
    import transcend as ts
    t = Timer()
    t.start()
    f = ts.Ffmpeg(loglevel='error', overwrite=True)
    # f.input = ts.protocol.S3In('s3://xfaps.queue/Sintel.2010.1080p.mkv')
    f.input = ts.protocol.S3In('s3://xfaps.queue/v1_v2_side_traj_SELECT.mov')
    # f.save(ts.preset.vpx.AnyDevice360p(output=ts.protocol.PipeOut()))
    # print(f.save(ts.preset.vpx.AnyDevice360p(output=ts.protocol.FileOut('test_files/test.vpx.webm'))))
    f.save(
        ts.preset.h264.AnyDevice(output=ts.protocol.FileOut('test_files/test/foo/fallback.mp4')),
        ts.preset.hls.H264xAnyDevice360p(output=ts.protocol.FileOut('test_files/test/foo/360.m3u8')),
        # ts.preset.h.H264xAnyDevice(output=ts.protocol.FileOut('test_files/test/240p.dash.mpd')),
        ts.preset.hls.H264x720p(output=ts.protocol.FileOut('test_files/test/foo/720.m3u8')),
        ts.preset.hls.H264x1080p(output=ts.protocol.FileOut('test_files/test/foo/1080.m3u8')),
        # ts.Audio(
        #     disable_video=True,
        #     disable_subtitles=True,
        #     codec=ts.preset.hls.LoFiHlsAudio.__class__(flags='cgop', key_interval=120, min_key_interval=120),
        #     format=ts.format.Mp4(movflags='frag_keyframe+faststart'),
        #     output=ts.protocol.FileOut('test_files/test.audio.hev2.m4a')
        # ),
        # ts.Audio(
        #     disable_video=True,
        #     disable_subtitles=True,
        #     codec=ts.preset.hls.HiFiHlsAudio.__class__(flags='cgop', key_interval=120, min_key_interval=120),
        #     format=ts.format.Mp4(movflags='frag_keyframe+faststart'),
        #     output=ts.protocol.FileOut('test_files/test.audio.hev2.hi.m4a')
        # )
    )
    print(t.stop())
