


export const sleepFunc = (sleepMillis:number) => {
  return new Promise((resolve, reject) => {
    setTimeout(()=> resolve("DONE"), sleepMillis)
  })
};

export const makeDummyApi = async (data:Object, delayMillis:number) => {
  if(delayMillis === undefined)
    await sleepFunc(1000)
  else
    await sleepFunc(delayMillis)

  return {status: "SUCCESS", data: data}

}
