# MDRS_monitoring_overlay
Purdue MDRS raspberry pi hosted remote station monitoring system. This project is intended to use 10 rasperry pi pico w controllers spread throughout the MDRS campus to send information to an adafruit dashboard to display air quality data and airlock status, potentially with EVA suit charge status, crew logs, and reports also included.

This repo contains schematics and software
  - While MDRS crews are on site sim should be maintained by respecting the ~22 minute lag time between mission control updates and pulling anything from the repo

### What is done
Code available on this github allows for updating an adafruit dashboard from a raspberry pi pico w controller using the umqtt.simple mqtt library.

Two air quality monitoring modules have been constructed and tested at the MDRS station.

### Needs to be done
Mqtt library (umqtt.simple) now returns an error ([Errno 9] EBADF) when connecting to dashboard after several days of successful testing for unknown reasons, this must be fixed before further expanding sensor network.

Temperature / humidity sensors could not be detected with I2C during initial testing, this must be fixed to allow for accurate data collection.

No airlock sensors have been constructed at MDRS, though the requisite parts should be present at the station. (reed switches and magnets) The code for these should function nearly identically to the air quality code however, and there is a nearly complete example in this repo.

AA Batteries have been used to power pico w boards for sensor testing, and many are present at the station, but it requires a pack of several to be used for an effective amount of time. We instead recommend looking at micro usb cable to permanant wall fixture where possible, and rechargable battery packs when it's not.

The two prototype air sensors do not have permanant casing solutions, one is mounted to a cardboard testing mount and the other has no mounting. A permanent and robust system is needed instead. The entire pi board and sensor system take up abot 1 square foot when laid out comfortably, the airlock system only requires the board and reed switches so it takes up much less room.

Other features that could be implimented include water tank monitoring, EVA suit status, and adding crew logs / research updates into the dashboard. (TODO on whether or not the materials on the station can do this, or if more are needed)

## Air quality sensors
Reading from 5 air quality sensors (with datasheets)
 - temp / humidity (combined in one sensor) (currently not utilized in software due to problems with I2C connection, temporarily replaced with onboard temperature sensor)
   - http://aosong.com/userfiles/files/media/Data%20Sheet%20AHT21.pdfhttp://aosong.com/userfiles/files/media/Data%20Sheet%20AHT21.pdf 
 - CO2
   - https://cdn-reichelt.de/documents/datenblatt/C150/MH-Z19C-PC_DATENBLATT.pdf
 - PM2.5
   - https://wiki.keyestudio.com/Ks0196_keyestudio_PM2.5_Shield
 - VOC
   - https://www.winsen-sensor.com/d/files/zp07-mp503-10-grade-manual-air-quality-detection-module-1_3-terminal-forward.pdf
 - Ozone
   - https://cdn.sparkfun.com/assets/9/9/6/e/4/mq131-datasheet-low.pdf

## Project goals
10 raspberry pi pico w controllers throughout station measuring air quality, airlock status, and EVA suit status

5 controllers used for air quality monitoring, 1 in each of the MDRS buildings
 - RAM
 - Hab floor 1
 - Hab 2
 - Science Dome
 - Greenhab
   
5 controllers measuring airlock status using reed switches and magnets
 - One pi in each of the airlocks / doors on campus to measure these

Measuring EVA suit charge status using GPIO voltage detection
 - Not yet implimented, but suit status currently manually measured with a multimeter, so another board could be used to monitor suit status using an ADC

## Setup Instructions
Install Thonny [https://thonny.org]
 - Connects and flashes code to the raspberry pi boards very easily

Download pico firmware at [https://rpf.io/pico-w-firmware](https://rpf.io/pico-w-firmware)

Running Code from this repository (Instructions mainly from https://projects.raspberrypi.org/en/projects/get-started-pico-w/1)
  1. Clone git directory
  2. Connect pico to computer via micro usb
  3. Place firmware file into pico drive folder (You can literally just drag it)

     - pico folder in your file explorer should disappear
  
  4. Bottom right corner of Thonny shows what editor is being used, you should be able to select  ‘MicroPython (Raspberry Pi Pico)’ 
  5. Use save as in Thonny to save necessary code onto pico
    - keep in mind main.py always runs on pico boot

SecurityInfo
  - When you add your code to the pico make sure to also add securityInfo.py
  - securityInfo.py is ignored by git so you need a local copy that contains...

    ssid = "wifi name"  
    
    wifi_password = "wifi password"
    
    website_password = "website_password"
    
    mqtt_username
    
    mqtt_password

    mqtt_client_id
    
    all mqtt_topics

## Adafruit dashboard setup
adafruit_sensor_logging.py calls the read"X".py functions to read various sensor values based off the schematics above.

1) To use it copy all the required files onto the pico w then rename adafruit_sensor_logging.py to main.py.

2) Configure securityInfo.py

3) Run it once connected to a machine where you can see terminal output to ensure it's working.
4) check adafruit dashboard to ensure auto logging and manual updates both work
5) When running code on the board the connected LED should stay on while connecting to internet, then flash every 5 seconds once setup is successful
  - If the LED flashed 10 times rapidly after attempting connection then there was an error when connecting, reboot and try again and / or use the terminal to see the error codes and debug

#### Local Sensor Log Setup

CollectSensorData.py is a function that calls the read"X".py values in the repo above every hour and saves them into a timestamped csv file.

  
Setup instructions
1. Save the file onto the pico board
2. Rename it to main.py so that it runs on startup.
3. Copy the read"X".py files from the github, currently makes calls to following
    - readCO2
    - readOnboardTemp
    - readPM2_5
    - readVOC
4. To collect sensor data connect back to the pi via micro usb and download the csv files (should be a seperate file for each sensor)

## Website Features and GUI format
Sensor dashboard accessable at io.adafruit.com using Purdue MDRS credentials

Dahsboard is customizable to allow for text and buttons to be added
- TODO we could use these features to log off-nominal systems, research / EVA logs, and other crew logs that are be remotely accessible 
