const tonePositive = new Audio('/audio/tick-right.ogg');
const toneNegative = new Audio('/audio/tick-wrong.ogg');
const toneCombo = new Audio('/audio/tick-right-combo.ogg');
const tonePointEarn = new Audio('/audio/point-earn-2.mp3');
const toneTopicComplete = new Audio('/audio/topic-complete.mp3');
const toneXpEarn = new Audio('/audio/xp-earn.mp3')
const toneXpCount = new Audio('/audio/xp-count.mp3')
//const toneUpNext = new Audio('statics/audio/up-next.mp3')

/*export function playTone(toneName$){
  let tone = `statics/audio/${toneName$}`
  return new Audio(tone).play();
}*/

class ToneAudio{
  static playPositive(){
    return tonePositive.play() //playTone('tick-right.ogg')
  }

  static playNegative(){
    return toneNegative.play() //playTone('tick-wrong.mp3')
  }
  static playPointEarn(){
    return tonePointEarn.play()
  }
  static playTopicComplete(){
   return toneTopicComplete.play()
  }

  static playXPEarn(){
    return toneXpEarn.play();
  }
  static playXPCount(){
    return toneXpCount.play();
  }
}

export  default ToneAudio;

export  {tonePositive, toneNegative, tonePointEarn}
