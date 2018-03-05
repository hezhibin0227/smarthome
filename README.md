# smarthome
my smart home project (include weChat, Raspberry Pi GPIO with RGB LED and DHT11, Redis, S3 object store, tuling123 serivce )

wxMain.py
Main program, popup the login QR code. Listen to the weChat input then pass the input to messageHandler or upload content to ECS test drive.

messageHandler.py
According to the received input, instruct RaspberryPi to control omxPlayer or control the RGB LED.

omxController.py
Generate the mp3 list and invoke the omxPlayer functions: Play/Stop/Volume+/Volume-. 

objStore.py
Upload the received content (Picture/Video/Recording/Doc) to ECS Test Drive.

chatRobot.py
AI chat robot, provide AI chat response.

redisStore.py
Write and read Redis on PWS.

RGBController.py
Control the  RGB LED on/off and it¡¯s colors.

DHT11.py
Standalone app to continuously read DHT11 sensor data and write them to Redis on PWS, which is deployed in Raspberry Pi.

flaskServer.py
Standalone web app to read the RGB LED and DHT11 data stored in Redis then render them to browser, which is deployed in PWS.

mainpage.html
Main page for query smart home status.

results.html
Result rendering page to display sensor data.


