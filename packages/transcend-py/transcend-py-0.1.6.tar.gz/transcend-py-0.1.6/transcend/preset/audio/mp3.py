from ...codec import *


#: Audio presets
LoFiAudio = Mp3(bitrate='64k', sample_rate='44100', channels=2)
MidFiAudio = Mp3(bitrate='128k', sample_rate='44100', channels=2)
HiFiAudio = Mp3(bitrate='320k', sample_rate='44100')
