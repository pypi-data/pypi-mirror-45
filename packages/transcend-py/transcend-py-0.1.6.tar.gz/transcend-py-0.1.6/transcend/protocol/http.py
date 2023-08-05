# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'HttpIn', 'HttpOut',


HTTP_OPT = [
    BoundedOpt('seekable', lower=-1, upper=1),
    EnableOpt('chunked_post', 'chunked'),
    Opt('content_type'),
    Opt('proxy'),
    Opt('headers'),
    EnableOpt('multiple_requests'),
    Opt('post_data'),
    Opt('user_agent'),
    IntOpt('timeout'),
    Flag('reconnect_at_eof'),
    Flag('reconnect_streamed'),
    IntOpt('reconnect_delay_max'),
    Opt('mime_type'),
    EnableOpt('icy'),
    Opt('icy_metadata_headers'),
    Opt('icy_metadata_packet'),
    Opt('cookies'),
    IntOpt('offset'),
    IntOpt('end_offset'),
    Opt('method'),
    IntOpt('listen')
]


class _Http(Protocol):
    """
    `HTTP access protocol`
    ~~~~~~~~~~~~~~~~~~~~~~
    @seekable: (#int) Control seekability of connection. If set to 1 the
        resource is supposed to be seekable, if set to 0 it is assumed not to
        be seekable, if set to -1 it will try to autodetect if it is seekable.
        Default value is -1.
    @chunked (chunked_post): (#bool) If set to 1 use chunked Transfer-Encoding
        for posts, default is 1.
    @content_type: (#str) Set a specific content type for the POST messages.
    @proxy (http_proxy): (#str) @et HTTP proxy to tunnel through e.g.
        http://example.com:1234
    @headers: (#str) Set custom HTTP headers, can override built in default
        headers. The value must be a string encoding the headers.
    @multiple_requests: (#bool) Use persistent connections if set to 1, default
        is 0.
    @post_data: (#str) Set custom HTTP post data.
    @user_agent: (#str) Override the User-Agent header. If not specified the
        protocol will use a string describing the libavformat build.
    @timeout: (#int) Set timeout in microseconds of socket I/O operations used
        by the underlying low level operation. By default it is set to -1,
        which means that the timeout is not specified.
    @reconnect_at_eof: (#bool) If set then eof is treated like an error and
        causes reconnection, this is useful for live / endless streams.
    @reconnect_streamed: (#bool) If set then even streamed/non seekable streams
        will be reconnected on errors.
    @reconnect_delay_max: (#int) Sets the maximum delay in seconds after which
        to give up reconnecting
    @mime_type: (#str) Export the MIME type.
    @icy: (#bool) If set to 1 request ICY (SHOUTcast) metadata from the server.
        If the server supports this, the metadata has to be retrieved by the
        application by reading the icy_metadata_headers and icy_metadata_packet
        options. The default is 1.
    @icy_metadata_headers: (#str) If the server supports ICY metadata, this
        contains the ICY-specific HTTP reply headers, separated by newline
        characters.
    @icy_metadata_packet: (#str) If the server supports ICY metadata, and
        icy was set to 1, this contains the last non-empty metadata packet
        sent by the server. It should be polled in regular intervals by
        applications interested in mid-stream metadata updates.
    @cookies: (#str) Set the cookies to be sent in future requests. The format
        of each cookie is the same as the value of a Set-Cookie HTTP response
        field. Multiple cookies can be delimited by a newline character.
    @offset: (#int) Set initial byte offset
    @end_offset: (#int) Try to limit the request to bytes preceding this offset.
    @method: (#str) When used as a client option it sets the HTTP method for
        the request. When used as a server option it sets the HTTP method that
        is going to be expected from the client(s). If the expected and the
        received HTTP method do not match the client will be given a Bad
        Request response. When unset the HTTP method is not checked for now.
        This will be replaced by autodetection in the future.
    @listen: (#int) If set to 1 enables experimental HTTP server. This can be
        used to send data when used as an output option, or read data from a
        client with HTTP POST when used as an input option. If set to 2 enables
        experimental mutli-client HTTP server. This is not yet implemented in
        ffmpeg.c or ffserver.c and thus must not be used as a command line
        option.
    """
    OPT = HTTP_OPT


class HttpIn(_Http):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class HttpOut(_Http):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
