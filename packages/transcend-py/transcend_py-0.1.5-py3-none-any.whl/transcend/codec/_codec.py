# -*- coding: utf-8 -*-
from ..cli import *
from ..probe import Probe


__all__ = (
    'Codec',
    'VideoCodec',
    'AudioCodec',
    'Quantizer',
    'BFrames',
    'IFrames',
    'CompareFunctions',
    'Macroblocks',
    'MotionEstimation'
)


DEFAULT_CODEC_OPT = [
    Opt('c', 'codec'),
    BitOpt('b', 'bitrate'),
    IntOpt('threads', default=0),
    BitOpt('maxrate', 'max_bitrate'),
    BitOpt('minrate', 'min_bitrate'),
    BitOpt('bufsize', 'buffer_size'),
    IntOpt('g', 'key_interval'),
    IntOpt('keyint_min', 'min_key_interval'),
    BitOpt('bt', 'bitrate_tolerance'),
    FlagsOpt('flags'),
    FlagsOpt('flags2'),
    IntOpt('frame_number'),
    OneOfOpt('strict', choices=('very', 'strict', 'normal',
                                'experimental')),
    OneOfOpt('err_detect',
             choices=('crccheck', 'bitstream', 'buffer', 'explode',
                      'ignore_err', 'careful', 'compliant',
                      'aggressive')),
    OneOfOpt('ec', 'error_concealment',
             choices=('guess_mvs', 'deblock', 'favor_inter')),
    IntOpt('bits_per_coded_sample'),
    IntOpt('rc_init_occupancy'),
    IntOpt('lowres'),
    IntOpt('skip_threshold'),
    IntOpt('skip_factor'),
    IntOpt('skip_exp'),
    IntOpt('slices'),
    Opt('sub_charenc')
]


class Codec(OptSet):
    '''
    -threads #int Use 0 for auto
    -maxrate #int (bit/s) Set the max bitrate tolerance. Requires -bufsize
                  option to be set.
    -minrate #int Set minimum bitrate tolerance (bit/s). Most useful in setting
                  up a CBR encode, otherwise it is of little use.
    -bufsize #int Set ratecontrol buffer size (in bits)
    -bt - bitrate tolerance in bit/s
    -flags flags (mv4|qpel|loop|qscale|gmc|mv0|input_preserved|pass1|pass2|gray|
                  emu_edge|psnr|truncated|naq|ildct|low_delay|global_header|
                  bitexact|aic|ilme|cgop)
    -frame_number #int Set the frame number
    -strict #int Specify how strictly to follow standards
                 (very|strict|normal|experimental)
    -err_detect Set error detection flags. (crccheck|bitstream|buffer|explode|
                ignore_err|careful|compliant|aggressive)
    -ec Set error concealment strategy (guess_mvs|deblock|favor_inter)
    -bits_per_coded_sample #int
    -rc_init_occupancy #int Set number of bits which should be loaded into the
                       rc buffer before decoding starts.
    -flags2 (fast|noout|ignorecrop|local_header|chunks|showall|expor_mvs)
    -profile #int
    -level #int
    -lowres #int Decode at 1 = 1/2, 2=1/4, 3=1/8 resolutions
    -skip_threshold #int Set frame skip threshold
    -skip_factor #int Set frame skip factor
    -skip_exp #int Skip frame exponent
    -slices #int Number of slices, used in parallelized encoding
    -sub_charenc Sets the input subtitles character encoding.
    -keyint_min #int Set minimum interval between IDR-frames
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_CODEC_OPT + self.OPT + list(opt)), **opts)

    def __call__(self, *args, **kwargs):
        return self.__class__(*args, **kwargs)


DEFAULT_VIDEO_OPT = [
    Opt('c:v', 'codec'),
    BitOpt('b:v', 'bitrate'),
    Opt('profile:v', 'profile'),
    Opt('level:v', 'level'),
    FloatOpt('r', 'frame_rate'),
    SizeOpt('s', 'size'),
    ByteOpt('ps', 'rtp_payload_size'),
    IntOpt('lelim', 'luminance_elim'),
    IntOpt('celim', 'chrominance_elim'),
    OneOfOpt(
        'dct',
        choices=(
            'auto',
            'fastint',
            'mmx',
            'altivec',
            'faan'
        )
    ),
    FloatOpt('rc_init_cplx', 'init_complexity'),
    FloatOpt('lumi_max', 'max_luminance'),
    FloatOpt('tcplx_mask', 'temporal_complexity'),
    FloatOpt('scplx_mask', 'spatial_complexity'),
    FloatOpt('p_mask', 'inter_masking'),
    FloatOpt('dark_mask', 'dark_masking'),
    IntOpt('idct', 'idct'),
    OneOfOpt(
        'pred',
        'prediction_method',
        choices=('left', 'plane', 'median')
    ),
    FloatOpt('aspect'),
    IntOpt('ibias', 'intra_quant_bize'),
    OneOfOpt(
        'coder',
        choices=('vlc', 'ac', 'raw', 'rle', 'deflate')
    ),
    IntOpt('context'),
    IntOpt('sc_threshold', 'scene_change_thresh'),
    IntOpt('lmin', 'min_lagrange'),
    IntOpt('lmax', 'max_lagrange'),
    IntOpt('nr', 'noise_reduction'),
    IntOpt('refs'),
    IntOpt('chromaoffset'),
    IntOpt('trellis'),
    IntOpt('sc_factor', 'scene_change_factor'),
    IntOpt('colorspace'),
    IntOpt('dc', 'dc_precision'),
    IntOpt('nssew', 'nsse_weight'),
    OneOfOpt(
        'field_order',
        choices=('progressive', 'tt', 'bb', 'tb', 'bt')
    ),
    OneOfOpt('skip_alpha', cast=int, choices=(0, 1))
]


class VideoCodec(Codec):
    '''
    -g #int Set the GOP size. (default is 12)
        (video)
    -ps #int Set RTP payload size in bytes
    -lelim #int Set single coefficient elimination threshold for luminance
    -celim #int Set single coefficient elimination threshold for chrominance
    -dct #int Set DCT algorithm (auto|fastint|int|mmx|altivec|faan)
    -rc_init_cplx #float Set initial complexity for 1-pass encoding.
    -lumi_max #float Compress bright areas stronger than medium was
    -tcplx_max #float Set temporal complexity masking
    -scplx_mask #float Set spatial complexity masking
    -p_mask #float Set inter masking
    -dark_mask #float Compress dark areas stronger than medium ones
    -idct #int Select IDCT implementation
    -pred #int Set prediction method. (left|plane|median)
    -aspect #float Set sample aspect ratio
    -last_pred #int Set amount of motion predictors from the previous frame.
    -coder #int (vlc|ac|raw|rle|deflate)
    -context #int Set context model
    -sc_threshold #int Set scene change threshold
    -lmin #int Set min lagrange factor
    -lmax #int Set max lagrange factor
    -nr #int Set noise reduction
    -refs #int Set reference frames to consider for motion compensation
    -chromaoffset #int Set chroma qp offset from luma
    -trellis #int Set rate-distortion optimal quantization.
    -sc_factor #int Set value multiplied by qscale for each from and added
                to scene_change_score
    -colorspace #int
    -dc #int Set intra_dc_precision
    -nssew #int Set nsse weight
    -field_order Set/override the field order of the video.
                (progressive|tt|bb|tb|bt)
    -skip_alpha #int Set to 1 to disable processing alpha (transparency)
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_VIDEO_OPT + self.OPT + list(opt)), **opts)


DEFAULT_AUDIO_OPT = [
    Opt('c:a', 'codec'),
    Opt('profile:a', 'profile'),
    Opt('level:a', 'level'),
    Opt('b:a', 'bitrate'),
    IntOpt('ar', 'sample_rate'),
    IntOpt('ac', 'channels'),
    IntOpt('aq', 'quality'),
    IntOpt('cutoff'),
    IntOpt('frame_size'),
    OneOfOpt(
        'audio_service_type',
        'service_type',
        choices=('ma', 'ef', 'vi', 'hi', 'di', 'co', 'em', 'vo', 'ka')
    )
]


class AudioCodec(Codec):
    '''
    -ar #int Set audio sampling rate in Hz
    -ac #int Set the number of audio channels
    -aq #int Set audio quality (codec-specific)
    -cutoff #int Set the cutoff bandwidth
    -frame_size #int Set the audio frame size. Each submitted frame
                except the last must contain exactly frame_size samples per
                channel
    -audio_service_type #int Set audio service type.
                        (ma|ef|vi|hi|di|co|em|vo|ka)
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_AUDIO_OPT + self.OPT + list(opt)), **opts)


DEFAULT_QUANTIZER_OPT = [
    BoundedOpt('qcomp', 'curve_compression', lower=0.0, upper=1.0, cast=float),
    FloatOpt('qblur', 'blur'),
    IntOpt('qmin', 'min'),
    IntOpt('qmax', 'max'),
    IntOpt('qdiff', 'max_diff'),
    IntOpt('ibias'),
    IntOpt('pbias')
]


class Quantizer(OptSet):
    '''
    -qcomp #float Quantizer-Curve Compression
    -qblur #float Set the video quantizer scale blur (VBR)
        (video)
    -qmin #int Set the minimum video quantizer scale (VBR) Must be included
          between -1 and 69, default value is 2.
        (video)
    -qmax #int Set max video quantizer scale (VBR). Must be included between
          -1 and 1024, default value is 31.
        (video)
    -qdiff #int Set the max difference between the quantizer scale (VBR)
        (video)
    -ibias #int Set intra quant bias
    -pbias #int Set inter quant bias
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_QUANTIZER_OPT + self.OPT + list(opt)), **opts)


DEFAULT_BFRAMES_OPT = [
    BoundedOpt('bf', 'max', lower=-1, upper=16, default=0),
    FloatOpt('b_qfactor', 'q_factor'),
    FloatOpt('b_qoffset', 'qp_offset'),
    OneOfOpt('b_strategy', 'strategy', cast=int, choices=(0, 1, 2))
]


class BFrames(OptSet):
    '''
    -bf #int Set the max number of B frames between non-B-frames. Must be an
        integer between -1 and 16. 0 means that B-frames are disabled. If a
        value of -1 is used, it will choose an automatic value depending on
        the encoder. Default is 0.
        (video)
    -b_qfactor #float Set qpfactor between P and B frames.
        (video)
    -b_qoffset #float Set QP offset between P and B-frames
        (video)
    -b_strategy #int Set strategy to choose between I/P/B-frames
        (video)
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_BFRAMES_OPT + self.OPT + list(opt)), **opts)


DEFAULT_IFRAMES_OPT = [
    FloatOpt('i_qfactor', 'q_factor'),
    FloatOpt('i_qoffset', 'qp_offset')
]


class IFrames(OptSet):
    '''
    -i_qfactor #float Set QP factor between P and I frames
        (video)
    -i_qoffset #float Set QP offset between P and I frames
        (video)
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_IFRAMES_OPT + self.OPT + list(opt)), **opts)


CF_CHOICES = (
    'sad', 'sse', 'satd', 'dct', 'psnr', 'bit', 'rd', 'zero',
    'vsad', 'vss3', 'nss3', 'wv53', 'w97', 'dctmax', 'chroma'
)

DEFAULT_CF_OPT = [
    OneOfOpt('cmp', 'pel_me', choices=CF_CHOICES),
    OneOfOpt('subcmp', 'sub_pel_me', choices=CF_CHOICES),
    OneOfOpt('mbcmp', 'macroblock_cmp', choices=CF_CHOICES),
    OneOfOpt('ildctcmp', 'interlaced_dct', choices=CF_CHOICES),
    OneOfOpt('precmp', 'pre_motion_est', choices=CF_CHOICES),
    OneOfOpt('skipcmp', 'skip', choices=CF_CHOICES)
]


class CompareFunctions(OptSet):
    '''
    -cmp #int Set full pel me compare function (sad(default)|sse|satd|dct|psnr|
              bit|rd|zero|vsad|vss3|nss3|wv53|w97|dctmax|chroma)
    -subcmp #int Set sub pel me compare function (sad(default)|sse|satd|dct|
                 psnr|bit|rd|zero|vsad|vss3|nss3|wv53|w97|dctmax|chroma)
    -mbcmp #int Set macroblock compare function (sad(default)|sse|satd|dct|
                psnr|bit|rd|zero|vsad|vss3|nss3|wv53|w97|dctmax|chroma)
    -ildctcmp #int Set interlaced dct compare function (sad(default)|sse|satd|
                   dct|psnr|bit|rd|zero|vsad|vss3|nss3|wv53|w97|dctmax|chroma)
    -precmp #int Set the pre motion estimation compare function
                 (sad(default)|sse|satd|dct|psnr|bit|rd|zero|vsad|vss3|nss3|
                  wv53|w97|dctmax|chroma)
    -skipcmp #int (sad(default)|sse|satd|dct|psnr|bit|rd|zero|vsad|vss3|nss3|
             wv53|w97|dctmax|chroma)
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_CF_OPT + self.OPT + list(opt)), **opts)


DEFAULT_MB_OPT = [
    OneOfOpt('mbd', 'decision_algo', choices=('simple', 'bits', 'rd')),
    IntOpt('mblmin', 'min'),
    IntOpt('mblmax', 'max'),
    IntOpt('mb_threshold', 'threshold'),
    IntOpt('skip_top'),
    IntOpt('skip_bottom'),
    FloatOpt('border_mask')
]


class Macroblocks(OptSet):
    '''
    -mbd #int Set macroblock decision algorithm (high quality mode)
              (simple|bits|rd)
    -mblmin #int Set min macroblock lagrange factor (VBR)
    -mblmax #int Set max macroblock lagrange factor (VBR)
    -mb_threshold #int Set macroblock threshold.
    -skip_top #int Set number of macroblock rows at the top which are skipped.
    -skip_bottom #int Set number of macroblock rows at the bottom which are
                 skipped.
    -border_mask #float Increase the quantizer for macroblocks close to borders.
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_MB_OPT + self.OPT + list(opt)), **opts)


DEFAULT_ME_OPT = [
    OneOfOpt(
        'me_method',
        choices=(
            'zero',
            'full',
            'epzs',
            'esa',
            'tesa',
            'dia',
            'log',
            'phods',
            'x1',
            'hex',
            'umh',
            'iter'
        )
    ),
    IntOpt('me_range'),
    IntOpt('dia_size'),
    IntOpt('pre_dia_size'),
    IntOpt('preme', 'pre'),
    IntOpt('subq', 'subq_est'),
    BoundedOpt('mepc', 'bitrate_penalty_comp', lower=1, upper=256),
    IntOpt('me_threshold', 'threshold')
]


class MotionEstimation(OptSet):
    '''
    -me_method Set motion estimation method. One of the most important
               settings for x264, both speed and quality-wise.
               (zero|full|epzs|esa|tesa|dia|log|phods|x1|hex|umh|iter)
    @me_range: (#int) MErange controls the max range of the motion search.
        For HEX and DIA, this is clamped to between 4 and 16, with a default
        of 16. For UMH and ESA, it can be increased beyond the default 16 to
        allow for a wider-range motion search, which is useful on HD footage
        and for high-motion footage. Note that for UMH and ESA, increasing
        MErange will significantly slow down encoding.
    -dia_size #int Set diamond type and size for motion estimation
    -pre_dia_size #int Set diamond type and size for motion estimation pre-pass
    -preme #int Set the pre motion estimation
    -subq #int Set sub pel motion estimation quality
    -mepc #int Set motion estimation bitrate penalty compensation (1.0 = 256)
    -me_threshold #int Set motion estimation threshold.
    '''
    OPT = []

    def __init__(self, *opt, **opts):
        super().__init__(*(DEFAULT_ME_OPT + self.OPT + list(opt)), **opts)
