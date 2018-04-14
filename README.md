# Xiaoyin's smart home project

![py27][py27]

Smart home project use weChat to communicate with Raspberry Pi, which will use GPIO to controll sensors and do some interesting things.

## Project Concept
<div align=left><img width="550" height="280" src="https://raw.githubusercontent.com/lxyoutlook/smarthome/master/common/images/concept.png"/></div>

## System Architecture
<div align=left><img width="650" height="300" src="https://raw.githubusercontent.com/lxyoutlook/smarthome/master/common/images/architecuture.png"/></div>

## Wechat UI
<div align=left><img width="200" height="350" src="https://raw.githubusercontent.com/lxyoutlook/smarthome/master/common/images/wechatUI.png"/></div>

## Web UI
<div align=left><img width="600" height="700" src="https://raw.githubusercontent.com/lxyoutlook/smarthome/master/common/images/WebUI.png"/></div>

## Code List
<div align=left><img width="600" height="300" src="https://raw.githubusercontent.com/lxyoutlook/smarthome/master/common/images/codelist.png"/></div>

## Usage
### ssh to your Raspberry PI
```Bash
python wxMain.py
```
```Bash
python DHT11.py
```
### Use Cloud Foundry CLI to push webapp to Pivotal Web Services
```Bash
cf push MonitorApp
```

## Thanks
Alberto Ramos (https://github.com/cermegno)

littlecodersh (https://github.com/littlecodersh)


