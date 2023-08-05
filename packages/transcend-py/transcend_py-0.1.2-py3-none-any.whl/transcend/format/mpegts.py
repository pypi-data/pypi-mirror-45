# -*- coding: utf-8 -*-
from ..cli import *
from ._container import *


__all__ = 'MpegTs',


class MpegTs(Container):
    """
    MPEG transport stream muxer.
    This muxer implements ISO 13818-1 and part of ETSI EN 300 468.


    `MPEGTS container format`
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    @original_network_id: (#int) Set the original_network_id
        (default 0x0001). This is unique identifier of a network in DVB.
        Its main use is in the unique identification of a service through
        the path Original_Network_ID, Transport_Stream_ID.
    @transport_stream_id: (#int) Set the transport_stream_id
        (default 0x0001). This identifies a transponder in DVB.
    @service_id: (#int) Set the service_id (default 0x0001) also known
        as program in DVB.
    @service_type: (#str) Set the program service_type
        (default digital_tv), see below a list of pre defined values.
    @pmt_start_pid: (#int) Set the first PID for PMT (default 0x1000,
        max 0x1f00).
    @start_pid number: (#int) Set the first PID for data packets
        (default 0x0100, max 0x0f00).
    @m2ts_mode: (#bool) Enable m2ts mode if set to 1. Default value is
        -1 which disables m2ts mode.
    @mux_rate (muxrate): (#int) Set a constant muxrate (default VBR).
    @pcr_period: (#int) Override the default PCR retransmission time
        (default 20ms), ignored if variable muxrate is selected.
    @pat_period : (#int) Maximal time in seconds between PAT/PMT tables.
    @sdt_period: (#int) Maximal time in seconds between SDT tables.
    @pes_payload_size: (#int) Set minimum PES packet payload in bytes.
    @mpegts_flags: (flags)
    @copyts: (#bool) Preserve original timestamps, if value is set to 1.
        Default value is -1, which results in shifting timestamps so that they
        start from 0.
    @tables_version: (#int) Set PAT, PMT and SDT version (default 0, valid
        values are from 0 to 31, inclusively). This option allows updating
        stream structure so that standard consumer may detect the change.
    """
    OPT = [
        Opt('f', 'format', value='mpegts'),
        IntOpt('mpegts_original_network_id', 'original_network_id'),
        IntOpt('mpegts_transport_stream_id', 'transport_stream_id'),
        IntOpt('mpegts_service_id', 'service_id'),
        Opt('mpegts_service_type', 'service_type'),
        IntOpt('mpegts_pmt_start_pid', 'pmt_start_pid'),
        IntOpt('mpegts_start_pid', 'start_pid'),
        EnableOpt('mpegts_m2ts_mode', 'm2ts_mode', lower=-1),
        IntOpt('muxrate', 'mux_rate'),
        IntOpt('pcr_period'),
        IntOpt('pat_period'),
        ByteOpt('pes_payload_size'),
        FlagsOpt('mpegts_flags'),
        EnableOpt('mpegts_copyts', 'copyts', lower=-1),
        BoundedOpt('tables_version', lower=0, upper=31)
    ]
