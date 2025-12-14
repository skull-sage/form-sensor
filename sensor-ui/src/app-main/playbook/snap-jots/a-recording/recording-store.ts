import {date} from "quasar"

export type ARecording = {
  id: string,
  title: string,
  blobList: Blob[]
}
export type RecordingDB = {
  docMap: Map<String, ARecording>,
  serial: number,
  nextId: ()=>string,
  save: ()=>void,
  get: (recordingId)=>ARecording,
  insert: (blobList, title)=>void,
  clear: ()=>void
  remove: (index:number)=>void
}

const DB:RecordingDB = {
  docMap: new Map<String, ARecording>(),
  serial: 0,

  nextId() {
    ++this.serial;
    return ""+this.serial
  },
  save() {
    // to be implemented with localstorage
  },

  get(recordingId)
  {
    return this.docMap.get(recordingId);
  },
  insert(blobList:Blob[], title:string) {
    const newId = this.nextId();
    if(!title)
      title = `New Recording ${newId} at ${date.formatDate(new Date(), "Do MMM, YYYY")}`

    const recording:ARecording = {
      id: newId,
      title: title,
      blobList: blobList
    }
    this.docMap.set(newId, recording);
    return newId;

  },

  remove(id:number) {
      this.docMap.delete(id);
  },

  clear() {
    this.docMap.clear();
  },
}

export default DB;
