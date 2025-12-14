import {  ContentOptions, CallbackOptions, RecorderEvents, DEFAULT_MIME_TYPE, StateEnum} from "./recording.types";





export default class SnapRecorder
{
  readonly recorder:MediaRecorder;

  #chunkList: Blob[];
  #totalRecordedBytes: number;
  //recorded size in bytes
  readonly timeSliceInSec: number;



  constructor(stream: MediaStream, contentOptions:ContentOptions, timeSliceSec, callbacks: CallbackOptions)
  {

    if(contentOptions === undefined || contentOptions.mimeType === undefined)
      throw new Error("options.content with mimeType must be provided");

    this.timeSliceInSec = timeSliceSec;
    this.recorder = new MediaRecorder(stream, contentOptions);
    this.#hookRuntime(callbacks);

  }



  // @ts-ignore
  #hookRuntime(options: RecorderOptions)
  {
    this.recorder.addEventListener(RecorderEvents.START, (evt) => {
      this.#chunkList = [];
      this.#totalRecordedBytes = 0;

      options.onStart(StateEnum[this.recorder.state])

    })


    this.recorder.addEventListener(RecorderEvents.DATA_AVAILABLE, (evt) => {
      //console.log("Data Available Time-Code: "+evt.timecode)
        this.#totalRecordedBytes += evt.data.size
        this.#chunkList.push(evt.data);
        const state:StateEnum = StateEnum[this.recorder.state];
        options.onProgress(this.#totalRecordedBytes, this.#chunkList,  state)
    });

    this.recorder.addEventListener(RecorderEvents.PAUSE, (evt) => options.onPause(evt))
    this.recorder.addEventListener(RecorderEvents.RESUME, (evt) => options.onResume(evt))

    this.recorder.addEventListener(RecorderEvents.STOP, (evt)=> {
      //const blob = new Blob(this.recordedChunks, {type: this.recorder.mimeType});
      options.onStop(this.#chunkList, this.recorder.mimeType)
    })

    this.recorder.addEventListener(RecorderEvents.ERROR, (evt) => options.onError(evt.error))
  }

  start() {
    if(this.timeSliceInSec)
      this.recorder.start(this.timeSliceInSec * 1000) // 10s
    else
      this.recorder.start()
  }

  pause(){
    this.recorder.pause();
  }

  resume(){
    this.recorder.resume();
  }

  stop(){
    this.recorder.stop();
  }


}
