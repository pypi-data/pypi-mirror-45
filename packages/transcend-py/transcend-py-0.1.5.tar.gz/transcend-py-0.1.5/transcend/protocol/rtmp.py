# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'RtmpIn', 'RtmpOut',


DEFAULT_RTMP_OPT = [
    Opt('username'),
    Opt('password'),
    Opt('app'),
    Opt('playpath'),
    EnableOpt('listen'),
    IntOpt('timeout'),
    IntOpt('rtmp_buffer', 'buffer'),
    Opt('rtmp_conn', 'conn'),
    Opt('rtmp_flashver', 'flashver'),
    IntOpt('rtmp_flush_interval', 'flush_interval'),
    Opt('rtmp_live', 'live'),
    Opt('rtmp_playpath', 'playpath'),
    Opt('rtmp_subscribe', 'subscribe'),
    Opt('rtmp_swfhash', 'swfhash'),
    Opt('rtmp_swfverify', 'swfverify'),
    Opt('rtmp_swfsize', 'swfsize'),
    Opt('rtmp_swfurl', 'swfurl'),
    Opt('rtmp_tcurl', 'tcurl')
]


class _Rtmp(Protocol):
    """
    `Real-Time Messaging Protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @username: (#str) An optional username (mostly for publishing).
    @password: (#str) An optional password (mostly for publishing).
    @app: (#str) It is the name of the application to access. It usually
        corresponds to the path where the application is installed on the RTMP
        server (e.g. /ondemand/, /flash/live/, etc.). You can override the
        value parsed from the URI through the rtmp_app option, too.
    @playpath: (#str) It is the path or name of the resource to play with
        reference to the application specified in app, may be prefixed by
        "mp4:". You can override the value parsed from the URI through the
        rtmp_playpath option, too.
    @listen: (#bool) Act as a server, listening for an incoming connection.
    @timeout: (#int) Maximum time to wait for the incoming connection. Implies
        listen.
    @buffer (rtmp_buffer): (#int) Set the client buffer time in milliseconds.
        The default is 3000.
    @conn (rtmp_conn): (#str) Extra arbitrary AMF connection parameters, parsed
        from a string, e.g. like B:1 S:authMe O:1 NN:code:1.23 NS:flag:ok O:0.
        Each value is prefixed by a single character denoting the type, B
        for Boolean, N for number, S for string, O for object, or Z for null,
        followed by a colon. For Booleans the data must be either 0 or 1 for
        FALSE or TRUE, respectively. Likewise for Objects the data must be 0 or
        1 to end or begin an object, respectively. Data items in subobjects may
        be named, by prefixing the type with ’N’ and specifying the name before
        the value (i.e. NB:myFlag:1). This option may be used multiple times to
        construct arbitrary AMF sequences.
    @flashver (rtmp_flashver): (#str) Version of the Flash plugin used to run
        the SWF player. The default is LNX 9,0,124,2. (When publishing, the
        default is FMLE/3.0 (compatible; <libavformat version>).)
    @flush_interval (rtmp_flush_interval): (#int) Number of packets flushed in
        the same request (RTMPT only). The default is 10.
    @live (rtmp_live): (#str) Specify that the media is a live stream. No
        resuming or seeking in live streams is possible. The default value is
        any, which means the subscriber first tries to play the live stream
        specified in the playpath. If a live stream of that name is not found,
        it plays the recorded stream. The other possible values are live and
        recorded.
    @pageurl (rtmp_pageurl): (#str) URL of the web page in which the media was
        embedded. By default no value will be sent.

    @playpath (rtmp_playpath): (#str) Stream identifier to play or to publish.
        This option overrides the parameter specified in the URI.
    @subscribe (rtmp_subscribe): (#str) Name of live stream to subscribe to.
        By default no value will be sent. It is only sent if the option is
        specified or if rtmp_live is set to live.
    @swfhash (rtmp_swfhash): (#str) SHA256 hash of the decompressed SWF
        file (32 bytes).
    @swfsize (rtmp_swfsize): (#str) Size of the decompressed SWF file,
        required for SWFVerification.
    @swfurl (rtmp_swfurl): (#str) URL of the SWF player for the media.
        By default no value will be sent.
    @swfverify (rtmp_swfverify): (#str) URL to player swf file, compute
        hash/size automatically.
    @tcurl (rtmp_tcurl): (#str) URL of the target stream. Defaults to
        proto://host[:port]/app.
    """
    OPT = DEFAULT_RTMP_OPT


class RtmpIn(_Rtmp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class RtmpOut(_Rtmp):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
