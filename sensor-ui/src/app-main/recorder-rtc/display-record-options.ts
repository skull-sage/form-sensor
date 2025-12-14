
export type DisplayRecordOptions = {

}

/**
 *  frame rate 30
 *  bitrate 1500
 *  video size 480p
 * */

export const InstaReel = {
  stream: {
    audio: {channelCount: 1},
    video: {
      width: 1080, //{ min: 640, ideal: 1920, max: 1920 },
      height: 1920, //{ min: 400, ideal: 1080 },
      frameRate: 30//{ max: 30 },
    }
  }
}
