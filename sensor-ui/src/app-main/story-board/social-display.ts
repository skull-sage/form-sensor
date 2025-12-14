

export default {
  facebook: {
    feed_landscape: {width: 1280, height: 720, aspectRatio: '16/9'}, // recommended
    feed_portrait: {width: 720, height: 1280, aspectRatio:'9/16'},
    stories: {width:1080, height: 1920, aspectRatio: '9/16', durationMaxSec: 90},
    collection: {width: 1200, height: 628, aspectRatio: '16/9'}
  },
  instagram: {
    feed_square: {width: 1080, height: 1080},
    feed_landscape: {width: 1080, height: 566},
    feed_portrait: {width: 1080, height: 1350},
    reels: {width: 1080, height: 1920, maxDuration: 90},
    stories: {width: 1080, height: 1920, maxDuration: 60}
  },
  youtube:{
    landscape: {width: 1920, height: 1080},
    square: {width: 1080, height: 1080},
    portrait: {width: 1080, height: 1920},
    videoAds: {width: 1920, height: 1080},
    shorts: {width: 1080, height: 1920}
  },
  linkedIn : {
    portrait : {width: 1024, height: 576, maxDuration: {desktop: '15m', mobile: '10m'}},
    landscape: {width: 576, height: 1024, maxDuration: {desktop: '15m', mobile: '10m'}},

  }
}
