## Concepts
- factors for video streaming: Frame Rate, Resolution and Bitrate.
- **Frame rate** is a rate at which the images or video frames are played to create motion. The frame rate is measured in frames per second (fps). The standard rate is 24fps for most video formats.
- **Video resolution** is the number of pixels that make up an image on your screen; video bitrate is the speed at which data is processed. Resolution is usually written as 720p or 1080p, referring to images that are either 720 pixels wide or 1,080 pixels wide.
- **Frame Rate** and **Resolution** are dependent on each other but bitrate is independent.
- **video bitrate** is the speed at which data is processed. The human eye might not be able to tell high bitrates apart, but processing hardware and software can: color grading or keying and compositing

## Reference Study Material
- Medium article - [ WebRTC quality: bitrate, resolution and frame rates](https://rtcwebdev.medium.com/webrtc-video-quality-bitrate-resolution-and-frame-rates-part-2-7b0c46807d90)
- restream - [Video bitrate](https://restream.io/learn/what-is/video-bitrate/)
- Adobe - [Explore Video Bitrate](https://www.adobe.com/au/creativecloud/video/discover/bit-rate.html)
- MDN - [Web Video Codec guide](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Formats/Video_codecs#choosing_a_video_codec)

Let’s say you want to stream on platforms like Facebook, YouTube or Twitch and expect the broadcast to be bufferless. Here are some insights on the best video bitrates to use:

- Full HD Video with a high frame rate (1080p, 60fps): bitrate should be **4,500-6,000 Kbps**
- Full HD with a standard frame rate (1080p, 30fps): bitrate should be **3,500-5,000 Kbps**
- Regular HD with high frame rate (720p, 60fps): your bitrate should be **3,500-5,000 Kbps**
- Regular HD with standard frame rate (720p, 30fps): your bitrate should be **2,500-4,000 Kbps**

NOTE: Loom seems to use **1500 bitrate**

## Live Saving Strategy (Loom)
- resolution matter but doesn't correspond to
- use bitrate of 1500
- how loom use ts encoding on the fly ? directly storing mp4 would be nice option

