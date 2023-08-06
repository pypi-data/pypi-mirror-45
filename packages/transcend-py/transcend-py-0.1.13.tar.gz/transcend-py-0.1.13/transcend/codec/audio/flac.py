# -*- coding: utf-8 -*-
"""
`FLAC`
============
libflac wrapper for FFMPEG
"""
from ...cli import *
from .._codec import *


__all__ = 'Flac',


class Flac(AudioCodec):
    """
    @compression_level: (#int) Sets the compression level, which chooses
        defaults for many other options if they are not set explicitly.
    @frame_size: (#int) Sets the size of the frames in samples per channel.
    @lpc_coeff_precision: (#int) Sets the LPC coefficient precision, valid
        values are from 1 to 15, 15 is the default.
    @lpc_type: (#str) Sets the first stage LPC algorithm. 'none', 'fixed',
        'levinson', 'cholesky'
    @lpc_passes: (#int) Number of passes to use for Cholesky factorization
        during LPC analysis
    @min_partition_order: (#int) The minimum partition order
    @max_partition_order: (#int) The maximum partition order
    @prediction_order_method: (#str) 'estimation', '2level', '4level', '8level',
        'search', 'log'
    @channel_mode (ch_mode): (#str) Sets channel mode; 'auto', 'indep',
        'left_side', 'right_side', 'mid_side'
    @exact_rice_parameters: (#bool) Chooses if rice parameters are calculated
        exactly or approximately. if set to 1 then they are chosen exactly,
        which slows the code down slightly and improves compression slightly.
    @multi_dim_quant: (#bool) Multi Dimensional Quantization. If set to 1 then
        a 2nd stage LPC algorithm is applied after the first stage to finetune
        the coefficients. This is quite slow and slightly improves compression.
    """
    OPT = [
        Opt('c:a', 'codec', value='libflac'),
        IntOpt('compression_level'),
        IntOpt('frame_size'),
        BoundedOpt('lpc_coeff_precision', lower=1, upper=15),
        OneOfOpt('lpc_type',
                 choices=('none', 'fixed', 'levinson', 'cholesky')),
        IntOpt('lpc_passes'),
        IntOpt('min_partition_order'),
        IntOpt('max_partition_order'),
        OneOfOpt('prediction_order_method',
                 choices=('estimation', '2level', '4level', '8level',
                          'search', 'log')),
        OneOfOpt('ch_mode', 'channel_mode',
                 choices=('auto', 'indep', 'left_side', 'right_side',
                          'mid_side')),
        EnableOpt('exact_rice_parameters'),
        EnableOpt('multi_dim_quant')
    ]
