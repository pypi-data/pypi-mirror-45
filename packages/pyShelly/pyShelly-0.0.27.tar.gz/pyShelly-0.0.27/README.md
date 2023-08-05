# pyShelly

Library for Shelly smart home devices. Using CoAP for auto discovery and status updates.

## Features

- Discover devices
- Monitor status
- Control (turn on/off etc)
- Run only locally
- Support user name and password
- Coexist with Shelly Cloud and Shelly app
- Support static and dynamic ip address
- Zero configuration

## Devices supported

- Shelly 1
- Shelly 2 (relay or roller mode)
- Shelly 4
- Shelly PLUG
- Shelly BULB
- Shelly RGBWW
- Shelly RGBW2
- Shelly H&T
- Shelly 2.5
- Shelly 2LED (not tested)
- Shelly PLUG S (not tested)

## Usage

```python
shelly = pyShelly()
shelly.cb_device_added.append(device_added)
shelly.open()
shelly.discover()

def device_added(dev):
  print (dev.devType)
```
