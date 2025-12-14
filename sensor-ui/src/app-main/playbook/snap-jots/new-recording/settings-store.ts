
import {reactive, markRaw} from 'vue'
import {findDisplayStream} from "@main/recorder-rtc/stream-funcs"
import { Notify } from 'quasar'

// Note: we will use StramTrack type instead of browser provided
// standard MediaStreamTrack will be used for UI interacttions only
export type DeviceInfo = {
  deviceId : string,
  label: string,
  kind: string
}

export type RecorderState = {
  cam: {
    stream: MediaStream,
    deviceList: DeviceInfo[],
    selectedId: string,
    error: Error
  },
  mic: {
    stream: MediaStream,
    deviceList: DeviceInfo[],
    selectedId: string,
    error: Error
  },
  display: {
    cameraOnly: boolean,
    stream: MediaStream // get full stream combined with audio and video
    error : Error
  }
}



export default class SettingsStore {

  state: RecorderState

  constructor() {
    this.state = reactive({
      //stream is selected stream by user
      cam: {
        stream: undefined,
        deviceList: [{deviceId:"NONE", kind: "videoinput", label: "No Camera"}],
        selectedId: undefined,
        error: undefined
      },
      mic: {
        stream: undefined,
        deviceList: [{deviceId:"NONE", kind: "audioinput", label: "No Microphone"}],
        selectedId: undefined,
        error: undefined
      },
      display: {
        cameraOnly: false,
        stream: undefined,
        error: undefined
      }
    })
  }

   async initDisplayRecording(){

    await this.tryCamStream(undefined); // trying default selection by browser
    await this.tryMicStream(undefined); // trying default selection by browser
    await this.enumerateUserDevices();

    await this.initDisplayStream();
  }

  async enumerateUserDevices(){
    try{
      const deviceList = await navigator.mediaDevices.enumerateDevices();
      deviceList.forEach(device => {
         if(device.kind === "videoinput"){
           this.state.cam.deviceList.push({deviceId: device.deviceId, kind: device.kind, label: device.label});
         }
         else if(device.kind === "audioinput"){
           this.state.mic.deviceList.push({deviceId: device.deviceId, kind: device.kind, label: device.label});
         }
      })
    }catch (error) {
      console.log(error);
      Notify.create({
        message: 'Error enumerating media devices',
        color: 'negative'
      })
    }

  }


  async initDisplayStream() {
    try{
      this.state.display.stream = await findDisplayStream();
    }catch (error) {
      this.state.display.error = error;
    }
  }

  // as an initial step we will try device = undefined to try default selection by browser
  async tryCamStream(device: DeviceInfo) {

      let constraints;
      if(device)
        constraints = { facingMode: "user", deviceId: { exact: device.deviceId } };
      else
        constraints = { facingMode: "user"};

      try{
        const stream = await navigator.mediaDevices.getUserMedia({ video: constraints});

        const {deviceId} = stream.getTracks()[0].getSettings(); // in case of initial undefined default selection
        this.state.cam.selectedId = deviceId;
        this.state.cam.stream = markRaw(stream);

      }catch(error){
        this.state.cam.error = error;
      }

  }
  async tryMicStream(device: DeviceInfo) {

    let constraints;
    if(device)
        constraints = { deviceId: {exact: device.deviceId}}
    else
        constraints = true;

    try{

      const stream = await navigator.mediaDevices.getUserMedia({ audio: constraints});
      const {deviceId} = stream.getTracks()[0].getSettings(); // in case of initial undefined default selection
      this.state.mic.selectedId = deviceId;
      this.state.mic.stream = markRaw(stream);
    }catch(error){
      this.state.mic.error = error;
    }
  }

  // closing mic and camera device
  closeDeviceOnNone(deviceState){
    console.log(this);
    this.closeStream(deviceState.stream);
    deviceState.stream = undefined;
    deviceState.selectedId = "NONE";
  }

  closeStream(stream: MediaStream) {
    if(stream){
      stream.getTracks().forEach(track => track.stop());
    }
  }

  close() {
    this.closeStream(this.state.cam.stream);
    this.closeStream(this.state.mic.stream);
    this.closeStream(this.state.display.stream);
  }

  getCombinedStream(){
    const streamList = [];
    if(this.state.cam.stream)
      streamList.push(this.state.cam.stream);
    if(this.state.mic.stream)
      streamList.push(this.state.mic.stream);
    if(this.state.display.stream)
      streamList.push(this.state.display.stream);

    return this.#mergeStream(streamList);
  }

  #mergeStream(streamList: MediaStream[]) : MediaStream {
    let stream: MediaStream;
    if(streamList.length === 1)
    {
      stream = streamList[0];
      debugger
    }
    else
    {
        stream = new MediaStream();
        streamList.forEach((s) => {
          s.getTracks().forEach((track) => {
            stream.addTrack(track);

          })
        })

      }

    console.log("### combined stream: tacklist");
    stream.getTracks().forEach(track => {
      console.log(track);
    })
    return stream;
  }
}
