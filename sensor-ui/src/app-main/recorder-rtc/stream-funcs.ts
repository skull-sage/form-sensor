




export const findDisplayStream =  async (systemAudio = 'include', surfaceSwitching = 'include') =>
{
    const streamOptions = {
      audio: {channelCount: 1},
      video: {frameRate: 30},
      systemAudio: 'include', // Display option says it doesn't have this though ?
      surfaceSwitching: surfaceSwitching,
      // It helps prevent accidental self capture and avoids the “Hall of Mirrors”
      selfBrowserSurface: 'include',

    }


    const stream:MediaStream = await navigator.mediaDevices.getDisplayMedia(streamOptions);

    console.log("# logging display stream")
    stream.getTracks().forEach(track => {
      console.log(track.getSettings())
      console.log(track.label)
    })

    return stream;
}

export const findMicTrackList = async ()=> {
    const deviceStreamOptions = {
      audio: true,
      //video: { facingMode: "user" }
    }

    const stream:MediaStream =  await navigator.mediaDevices.getUserMedia(deviceStreamOptions);
    return stream.getTracks();
}

export const findCamTrackList = async () => {
    const deviceStreamOptions = {
      video: { facingMode: "user" }
    }
    const stream:MediaStream =  await navigator.mediaDevices.getUserMedia(deviceStreamOptions);
    return stream.getTracks();
}


// as an example
export const printUserDevices = async ()=>{
  navigator
    .mediaDevices
    .enumerateDevices()
    .then((devices) => {
      console.log("# Enumerated devices: " + devices.length)
      devices.forEach((device) => {
        console.log(device);
      });
    })
    .catch((err) => {
      console.error(`${err.name}: ${err.message}`);
    });
}


