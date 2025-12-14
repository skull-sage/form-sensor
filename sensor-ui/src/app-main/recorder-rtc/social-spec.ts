

export type ReelVertical = {
  durationMaxSec: Number,
  resolutionH: 1080 | 720 | 480,
  aspectRatio: '9/16' | '1/1' | '4/5'
  frameRate:   30 | 60,

}

export const FbReel:ReelVertical = {
  durationMaxSec: 90,
  resolutionH: 720,
  aspectRatio: "9/16",
  frameRate: 60

}

export const LinkedInSquire:ReelVertical =
{
    durationMaxSec: 180,
    resolutionH: 480,
    aspectRatio: '1/1',
    frameRate: 30
}

export const LinkedInVerticle:ReelVertical =
  {
    durationMaxSec: 180,
    resolutionH: 480,
    aspectRatio: '4/5',
    frameRate: 30
  }

