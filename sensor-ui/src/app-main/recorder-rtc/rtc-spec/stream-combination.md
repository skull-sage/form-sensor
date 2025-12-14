
# Example 1

```js
const screenStream;
const micStream;
const remoteStream;
// merge audio from remote stream and micStream

const audioCtx = new AudioContext();
const source1 = audioCtx.createMediaStreamSource(micStream);
const source2 = audioCtx.createMediaStreamSource(remoteStream);
const destination = audioCtx.createMediaStreamDestination();

//connect sources to destination
// you can add gain nodes if you want
source1.connect(destination);
source2.connect(destination);

const outputStream= new MediaStream();
outputStream.addTrack(screenStream.getVideoTracks()[0]);
outputStream.addTrack(destination.stream.getAudioTracks()[0]);
```
