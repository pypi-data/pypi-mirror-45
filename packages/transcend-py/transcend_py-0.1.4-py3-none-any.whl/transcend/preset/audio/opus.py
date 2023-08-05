from ...codec import *


#: Audio presets
LoFiAudio = Opus(bitrate='64k', sample_rate='44100', channels=2)
MidFiAudio = Opus(bitrate='128k', sample_rate='44100', channels=2)
HiFiAudio = Opus(bitrate='320k', sample_rate='44100')
