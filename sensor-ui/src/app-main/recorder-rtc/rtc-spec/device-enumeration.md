


# Enumeration

The returned list will omit any devices that are blocked by the document
Permission Policy: microphone, camera, speaker-selection (for output devices), and so on.
Access to particular non-default devices is also gated by the
[Permissions API](https://developer.mozilla.org/en-US/docs/Web/API/Permissions_API),
and the list will omit devices for which the user has not granted explicit permission.

```js
  navigator
    .mediaDevices
    .enumerateDevices()
    .then((devices) => {
        devices.forEach((device) => {
        console.log(`${device.kind}: ${device.label} id = ${device.deviceId}`);
    });
  })
  .catch((err) => {
    console.error(`${err.name}: ${err.message}`);
  });
  ```

 if one or more MediaStreams are active or persistent permissions are granted:

```yaml
videoinput: FaceTime HD Camera (Built-in) id=csO9c0YpAf274OuCPUA53CNE0YHlIr2yXCi+SqfBZZ8=

audioinput: default (Built-in Microphone) id=RKxXByjnabbADGQNNZqLVLdmXlS0YkETYCIbg+XxnvM=

audioinput: Built-in Microphone id=r2/xw1xUPIyZunfV1lGrKOma5wTOvCkWfZ368XCndm0=
```

# media device constraints

Following the standard (which at this time requires using adapter.js in Chrome), to get a specific "videoinput" device, pass its deviceId into getUserMedia using the deviceId constraint:

```js
  navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    var camera = devices.find(device => device.kind == "videoinput");
    if (camera) {
      // ideal can be used instead of exact, but exact is more specific and faster, and it's what the standard requires.
      // exact is also required in Firefox, but ideal is fine in Chrome.
      var constraints = { deviceId: { exact: camera.deviceId } };
      return navigator.mediaDevices.getUserMedia({ video: constraints });
    }
  })
  .then(stream => video.srcObject = stream)
  .catch(e => console.error(e));
```

The `exact` keyword makes the constraint required, guaranteeing it'll return only the right one, or fail.

If you want two cameras, you'll have to call getUserMedia again with a different deviceId, and hope the OS you're on supports it (e.g. phones generally don't).
