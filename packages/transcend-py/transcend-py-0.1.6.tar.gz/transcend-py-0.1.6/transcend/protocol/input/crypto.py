# -*- coding: utf-8 -*-
from ...cli import *
from .._protocol import Protocol


__all__ = 'CryptoIn',


class CryptoIn(Protocol):
    """
    `AES-encrypted stream reading protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @key: (#str) Set the AES decryption key binary block from given hexadecimal
        representation.
    @iv: (#str) Set the AES decryption initialization vector binary block from
        given hexadecimal representation.
    """

    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value='crypto+' + endpoint),
            Opt('key'),
            Opt('iv')
            **opts
        )
