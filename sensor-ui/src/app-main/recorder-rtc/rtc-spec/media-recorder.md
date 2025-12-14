## Html5 MediaRecorder

Two constructor
  - `new MediaRecorder(stream:MediaStream)`
  - `new MediaRecorder(stream:MediaStream, options)`
  - Options can have props:
    - `mimeType` specifying format of resulting media
    - `audioBitsPerSecond` chosen bitrate for audio component
    - `videoBitsPerSecond` chosen bitrate for video component
    - `bitsPerSecond` inplace of above two; common bitrate for audio & video
    - `audioBitrateMode` can be `constant` or `variable` for complex signal
    - `videoKeyFrameIntervalDuration`
    - `videoKeyFrameIntervalCount`

### instance props
- `mimeType`, `stream`, `videoBitsPerSecond`, `audioBitsPerSecond`, `audioBitrateMode`
- `state` has value `{inactive, recording, paused}`


### instance methods
- `pause()` pauses recording & `resume()` resumes it
- `start()` starts recording; alternative `start(timeslice)` is more useful
   trigger `dataavilable` event containing `Blob` according to specified `timeslice`
- `stop()` completely stops recording firing a
`dataavailable` event containing the final `Blob` of saved data
- `requestData()`
  - requests `Blob` containing saved data;
  - fires `dataavialable` event
  - recording continues in new Blob

### static methods
`isTypeSupported(mimeType)`

### events
- `dataavailable`


example types are:
```
const types = [
  "video/webm",
  "audio/webm",
  "video/webm;codecs=vp8",
  "video/webm;codecs=daala",
  "video/webm;codecs=h264",
  "audio/webm;codecs=opus",
  "video/mp4",
];
```

https://stackoverflow.com/questions/44392027/webrtc-convert-webm-to-mp4-with-ffmpeg-js
https://stackoverflow.com/questions/79240257/how-to-make-webm-screen-recording-chunks-independently-processable-for-audio-ex
