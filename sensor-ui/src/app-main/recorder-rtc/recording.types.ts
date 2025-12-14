
export enum StateEnum {
  inactive = 'inactive',
  recording = 'recording',
  paused = 'paused'
}


/**
 *  for onComplete: instead of passing a single blob using new Blob(chunkList, mimeType)
 *  the client code is provided chunkList and defined mimeType for recorder enabling :
 *    - saving chunks for HLS streaming
 *    - video as a whole for other task
 * */


export type ContentOptions = {

    mimeType?: string,
    audioBitsPerSecond?: number,
    videoBitsPerSecond?: number,
    audioBitrateMode?: 'constant' | 'variable',
  }
//Example
  // mimeType: 'video/webm',
  // audioBitsPerSecond: 128000,
  // videoBitsPerSecond: 2500000,

export type  CallbackOptions = {
    onProgress: (recordedBytes:number, chunkList:Blob[], state: StateEnum) => void,
    onStart?: (state: StateEnum) => void,
    onStop?: (chunkList: Blob[], mimeType: string)  => void,
    onPause?: (evt: Event) => void,
    onResume?: (evt: Event) => void,
    // evt.error.name = SecurityError | InvalidModificationError | UnknownError
    onError?: (error: DOMException) => void,
}


export enum RecorderEvents
{
  DATA_AVAILABLE = "dataavailable",
  START = "start",
  STOP = "stop",
  PAUSE = "pause",
  RESUME = "resume",
  ERROR = "error",
}

export const DEFAULT_MIME_TYPE = "video/webm; codecs=h264,opus"
