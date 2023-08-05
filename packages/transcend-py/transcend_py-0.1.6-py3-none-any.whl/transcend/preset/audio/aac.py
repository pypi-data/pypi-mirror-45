from ...codec import *


#: Audio presets
LoFiAudio = Aac(bitrate='64k', sample_rate='44100', channels=2)
MidFiAudio = Aac(bitrate='128k', sample_rate='44100', channels=2)
HiFiAudio = Aac(bitrate='320k', sample_rate='44100')


#: HE-AAC audio presets
LoFiHeAudio = Aac(bitrate='24k', sample_rate='44100', channels=2,
                  profile='aac_he_v2')
# Not all devices can use he-aac audio but we should expect hi fi devices to be
# be able to at this point
MidFiHeAudio = Aac(bitrate='48k', sample_rate='44100', channels=2,
                   profile='aac_he_v2')
HiFiHeAudio = Aac(bitrate='160k', sample_rate='44100', profile='aac_he')
