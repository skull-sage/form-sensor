
import {reactive, shallowReactive} from "vue"


const URL = window.URL || window.webkitURL;
const Kbps = 1024;
const Mbps = Kbps * Kbps;
const Sec = 1000;// milliseconds

// for standard recording according to gathered knowledge
const CONTENT_OPTIONS = {
  mimeType: 'video/webm; codecs="av01.2.19H.12.0.000.09.16.09.1, opus"', // 4 - 6.9mb size
 // mimeType: 'video/webm; codecs="h264, opus"',
 // mimeType: 'video/mp4;codecs=avc1.42E01F,mp4a.40.2',
  bitsPerSecond:  1500 * Kbps, // MDN recommendation 800 * Mbps,
  audioBitrateMode: 'constant'
}

export enum RuntimeState {
  NOT_STARTED = 'not_started',
  RECORDING = 'recording',
  PAUSED = 'paused',
  STOPPED = 'stopped',
}

export type ChunkInfo = {
  data: Blob,
  duration?: number, // in seconds
}

export type RecorderState = {
  runtimeState: RuntimeState,
  totalWatchTime: number, // this is according to video object
  chunkList: Blob[],
  totalRecordedBytes: number
}

export type RecorderCallbacks = {
  onNextChunk: (blob: Blob) => void,
  onStart: () => void,
  onStop: () => void,
  onPause: () => void,
  onResume: () => void
}



export default class ScreenRecorder {
  runtimeState: RuntimeState;
  recorder : MediaRecorder
  timeSliceInSec: number = 1*Sec; // default to 1s
  stream: MediaStream;
  timeOutId: number;
  callbacks: RecorderCallbacks;

  constructor(stream: MediaStream, timeSlice:number, recoderCallbacks: RecorderCallbacks) {

      if(stream === undefined)
        throw new Error('no stream provided');

      this.stream = stream;
      this.callbacks = recoderCallbacks;

      this.timeSliceInSec = timeSlice*Sec;
    //  this.recorder = new MediaRecorder(stream, CONTENT_OPTIONS);
      this.runtimeState = RuntimeState.NOT_STARTED;
     // this.#hookCallbacks(this.state, this.recorder);
  }

  start(){
    if(this.runtimeState !== RuntimeState.NOT_STARTED)
      throw new Error('recorder already started & current state: ' + this.runtimeState);


    this.runtimeState = RuntimeState.RECORDING
    this.callbacks.onStart();

     this.startReadingContineous();
    //this.startReadingByChunk();
  }

  // will read each data fragment of the same recorded video
  startReadingContineous(){
    this.recorder = new MediaRecorder(this.stream, CONTENT_OPTIONS);
    this.recorder.start(5*Sec);

    this.recorder.ondataavailable = (evt) => {
      if (evt.data.size > 0) {
          this.callbacks.onNextChunk(evt.data) //this.state.chunkList.push({ data: evt.data, duration: undefined, timeCode: evt.timecode });
      }
    }

    this.recorder.onstop = (evt) => {
      this.recorder.ondataavailable = null;
      this.recorder = undefined;
      this.callbacks.onStop();
    }
  }

  // will read the recorded data as independent video chunk
  startReadingByChunk(){
    this.recorder = new MediaRecorder(this.stream, CONTENT_OPTIONS);
    this.recorder.start(1*Sec);
    const blobList:Blob[] = [];
    const startTiming = performance.now();
    this.recorder.ondataavailable = (evt) => {
      console.log("elapsed time for small blobk", (performance.now() - startTiming)/Sec, "sec", "blob size", evt.data.size, "bytes", "blob type", evt.data.type)
      if (evt.data.size > 0) {
          blobList.push(evt.data) //this.state.chunkList.push({ data: evt.data, duration: undefined, timeCode: evt.timecode });
      }

      if(this.runtimeState === RuntimeState.STOPPED)
      { // the recorder.stop() was already called by ScreenRecorder client
        this.callbacks.onNextChunk(new Blob(blobList, {type: CONTENT_OPTIONS.mimeType}));
        this.recorder.ondataavailable = null;
        this.recorder = undefined;
        this.callbacks.onStop();
      }
      else if(blobList.length == 10 && this.runtimeState === RuntimeState.RECORDING){

        console.log("elapsed time for chunk", (performance.now() - startTiming)/Sec, "sec")
        this.callbacks.onNextChunk(new Blob(blobList, {type: CONTENT_OPTIONS.mimeType}));
        this.recorder.ondataavailable = null;
        this.recorder.stop();
        this.recorder = undefined;

        this.startReadingByChunk(); // recording continues for next chunk

      }


    }; // ondata-available ends

  }


  stop(){
    // evading recorder-stop-listener: intentionally stopping the stream
    this.recorder.stream.getTracks().forEach(track => track.stop());
    this.recorder.stop();
    this.runtimeState = RuntimeState.STOPPED;

  }

  pause(){
    this.recorder.pause();
    this.callbacks.onPause(); // notifying the caller about the paused dat
  }
  resume(){
    this.recorder.resume();
    this.callbacks.onResume();
  }


  /* #hookCallbacks(state: RecorderState, recorder: MediaRecorder) {

    recorder.onstart = (e) => {
      state.runtimeState = RuntimeState.RECORDING;
    }

    recorder.ondataavailable = (e) => {

      state.runtimeState = RuntimeState.RECORDING;

      if (e.data.size == 0) return;

      state.chunkList.push({ data: e.data, duration: undefined, timeCode: e.timecode });

    };
    recorder.onstop = (e) => {

      if(this.onStop)
        this.onStop(this.state.chunkList);
      state.runtimeState = RuntimeState.STOPPED;

    }
    recorder.onpause = (e) => {
      state.runtimeState = RuntimeState.PAUSED;
    }
    recorder.onresume = (e) => {
      state.runtimeState = RuntimeState.RECORDING;
    }
  } */



}

/* export async function getBlobDuration(blob) : Promise<number> {
  const tempVideoEl = document.createElement('video')

  const durationP:Promise<number> = new Promise((resolve, reject) => {
    tempVideoEl.onloadedmetadata = () => {
      // Chrome bug: https://bugs.chromium.org/p/chromium/issues/detail?id=642012
      if(tempVideoEl.duration === Infinity) {
        tempVideoEl.currentTime = Number.MAX_SAFE_INTEGER
        debugger;
        tempVideoEl.ontimeupdate = () => {
          tempVideoEl.ontimeupdate = null
          resolve(tempVideoEl.duration)
          tempVideoEl.currentTime = 0
          debugger;
        }
      }
      // Normal behavior
      else{
        resolve(tempVideoEl.duration)
      }
      URL.revokeObjectURL(tempVideoEl.src);
      tempVideoEl.onloadedmetadata = null;

    };
    tempVideoEl.onerror = (event) => reject(event.target.error)
  })

  // const blobWithMime = new Blob([blob], {
  //   type: OPTIONS.mimeType,
  // });
  tempVideoEl.src =  URL.createObjectURL(blob)

  return durationP
} */
