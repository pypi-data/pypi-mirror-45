import math
import humanfriendly
from pathlib import Path

__all__ = 'calc_gop', 'to_k', 'calc_buffer_size', 'calc_scale'


def calc_gop(bitrate, frame_rate, min_gop=-1):
    # https://github.com/vbence/stream-m#fragments
    return max(math.ceil((200 * 8000) / ((bitrate / 1000) * frame_rate)), min_gop)


def to_k(bytes):
    return f'{int(math.ceil(bytes / 1000))}k'


def calc_buffer_size(bitrate):
    if isinstance(bitrate, int):
        return to_k(bitrate * 1.5)
    return to_k(humanfriendly.parse_size(bitrate) * 1.5)


def calc_scale(size):
    in_w, in_h = size.split('x')
    return f'trunc({in_w}/2)*2:trunc({in_h}/2)*2'


'''
create_m3u8_master(presets.h264.H264xAnyDevice(), )
'''
