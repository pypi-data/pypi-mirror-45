from ...codec import *


#: Audio presets
LoFiAudio = Vorbis(bitrate='64k', sample_rate='44100', channels=2)
MidFiAudio = Vorbis(bitrate='128k', sample_rate='44100', channels=2)
HiFiAudio = Vorbis(bitrate='320k', sample_rate='44100')
