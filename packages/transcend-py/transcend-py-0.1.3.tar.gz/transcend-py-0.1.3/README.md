# Transcend
`pip install transcend`


## What is transcoding?

Transcoding is unpacking one video compression format into another. Transcoding
involves completely changing the underlying video codec and in some cases
inolves changing the container.

The reasons for transcoding a format deal with compression and device support
for the various codecs. In order for a device to interpret a file, it must
contain a demuxing algorithm for that file's container. Additionally, the
device must possess a decoding algorithm which reads the incoming raw bitstream
(Audio, Video, or both) from the demuxer and generate the frames which are then
presented on the screen, or the sounds which are presented to your speakers.


### What about transmuxing?

Transmuxing is the process of changing the container format of a video or audio
file while preserving some or all of the streams from the original file.

For instance, H.264 video and AAC/MP3 audio tracks from MP4/MOV containers can
be transmuxed to segmented MP4/TS containers if certain conditions are met.

Because the underlying media streams are not changed, transmuxing is magnitudes
faster than transcoding.


#### Transmuxing requires

For video:
- MP4/MOV container format
- H.264 codec
- No b-frames are used

For Audio:
- MP4/MOV container format
- AAC or MP3 codec

For Segmenting/Fragmenting:
- Maximum GOP (group of pictures) should be less than or equal to the segment
  duration
- HE-AAC-V2 may not be used


## Important Definitions

* #### Container
  A container format is a set of instructions which define how different
  data and metadata coexist in a file. MP4, for example, is a multimedia
  container format most commonly used to store video and audio, but can also
  be used to store other data such as subtitles and still images. Since audio
  and video streams can be coded and decoded with many different algorithms,
  a container format may be used to provide a single file format
  to the user. Device manufacturers ultimately select which codecs are
  supported. These decisions are sometimes related to the underlying
  CPU architecture of the device, and in some cases patents and licensing
  agreements. The patent issue has spurred the creation of open container
  formats and codecs, such as WebM (container) and VPX (codec).

  Container formats only define how to store things within them, not what kinds
  of data are stored.

  MP4, AVI, WEBM, and OGG are example containers.

* #### Codec
  A codec is a compression algorithm which encodes (compresses)
  data and decodes (decompresses) data. Codecs are almost always lossy as
  a result of this compression, meaning that some data from the original video
  is 'lost' in the process of compression, resulting in a decompression which
  has a somewhat lower quality than the original video. H.264, H.265/HEVC, VPX,
  AAC and VORBIS are example codecs.

* #### Bitrate
  Bitrate in multimedia terminology represents the amount of data stored per
  second of duration. That is, a 64k bit rate means that media stores 64
  kilobits of information for each second of the media's runtime/duration. As
  such, you can estimate the file size of a given video or audio output based
  upon its bitrate. You simply need to multiply the bitrate by the media's
  duration. When dealing with audio, the number of channels also needs to be
  taken into account.

* #### Frame rate
  Frame rate refers to the frequency with which a video encoding's frames are
  displayed to the user over a given period of time. In most cases, the unit of
  time is 'seconds' and therefore we end up with 'frames per second' or 'fps'.
  The human visual system can theoretically process 1000 separate images per
  second but is not noticeable to the untrained eye after about 150. Current
  virtual reality headsets operate at a frame rate of 90 fps or 90 Hz.

  Typically, web videos are encoded to a frame rate of either 29.97
  (sometimes referred to as 30). Services like YouTube allow for a maximum
  frame rate of 60. The reason for this is that most devices don't allow for
  frame rates above 30 or 60 Hz due to energy constraints.

  For videos transcoded at resolution below 720p, a frame rate above 30 is
  probably not necessary, because the extra motion blur associated with the
  lower frame rates is far less noticeable.


-----------------
©2016 MIT License
