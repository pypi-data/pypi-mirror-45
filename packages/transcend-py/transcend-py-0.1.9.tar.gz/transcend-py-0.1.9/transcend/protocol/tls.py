# -*- coding: utf-8 -*-
from ..cli import *
from ._protocol import Protocol


__all__ = 'TlsIn', 'TlsOut',


TLS_OPT = [
    Opt('ca_file'),
    Opt('cert_file'),
    Opt('key_file'),
    EnableOpt('tls_verify', 'verify'),
    EnableOpt('listen')
]


class _Tls(Protocol):
    """
    `Transport Layer Security (TLS) protocol`
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @ca_file: (#str) A file containing certificate authority (CA) root
        certificates to treat as trusted. If the linked TLS library contains
        a default this might not need to be specified for verification to work,
        but not all libraries and setups have defaults built in. The file must
        be in OpenSSL PEM format.
    @cert_file: (#str) A file containing a certificate to use in the handshake
        with the peer. (When operating as server, in listen mode, this is more
        often required by the peer, while client certificates only are mandated
        in certain setups.)
    @key_file: (#str) A file containing the private key for the certificate.
    @verify (tls_verify): (#bool) If enabled, try to verify the peer that we
        are communicating with. Note, if using OpenSSL, this currently only
        makes sure that the peer certificate is signed by one of the root
        certificates in the CA database, but it does not validate that the
        certificate actually matches the host name we are trying to connect
        to. (With GnuTLS, the host name is validated as well.)
    @listen: (#bool) If enabled, listen for connections on the provided port,
        and assume the server role in the handshake instead of the client role.
    """
    OPT = TLS_OPT


class TlsIn(_Tls):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('i', 'endpoint', value=endpoint),
            **opts
        )


class TlsOut(_Tls):
    def __init__(self, endpoint, *opt, **opts):
        super().__init__(
            *opt,
            Opt('', 'endpoint', value=endpoint),
            **opts
        )
