# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'IcecastOut',


class IcecastOut(Protocol):
    """
    `Icecast output protocol.`
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Streams to icecast servers.

    @genre (ice_genre): (#str) Set the stream genre
    @name (ice_name): (#str) Set the stream name
    @description (ice_description): (#str) Set the stream description
    @url (ice_url): (#str) Set the stream website URL.
    @public (ice_public): (#bool) Set if the stream should be public.
        The default is 0 (not public).
    @user_agent: (#str) Override the User-Agent header. If not specified a
        string of the form "Lavf/<version>" will be used.
    @password: (#str) Set the Icecast mountpoint password.
    @content_type: (#str) Set the stream content type. This must be set if it
        is different from audio/mpeg.
    @legacy_icecast: (#bool) This enables support for Icecast versions < 2.4.0,
        that do not support the HTTP PUT method but the SOURCE method.

    """
    OPT = [
        Opt('ice_genre', 'genre'),
        Opt('ice_description', 'description'),
        Opt('ice_name', 'name'),
        Opt('ice_url', 'url'),
        EnableOpt('ice_public', 'public'),
        Opt('user_agent'),
        Opt('password'),
        Opt('content_type'),
        EnableOpt('legacy_icecast')
    ]

    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value='icecast://' + endpoint),
            **opts
        )
