

Here is some sample code:
to use WebAudio and a gain filter to adjust the volume
to set the volume of an audio/video tag (on the receiving end)

```js
var audioContext = new AudioContext();
var sourceStream = audioContext.createMediaStreamSource(yourStream);
var gain = audioContext.createGain();
sourceStream.connect(gain);
gain.value = 0.9;
gain.connect(audioContext.destination);
//and then use
audioContext.createMediaStreamDestination().stream
//. yourStream is the original stream that you got from getUserMedia().
```
