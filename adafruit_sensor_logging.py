import machine
import time
import network
from umqtt.simple import MQTTClient

try:
    import readCO2
    import readVOC
    import readPM2_5
    import readOnboardTemp
    import securityInfo
except ImportError as e:
    raise ValueError("Required files not found on local board: {}".format(e))

def get_last_csv_item(csv):
    csvdata=[]
    with open(csv, 'r') as input_file:
        for line in input_file:
            csvdata.append(line.rstrip('\n').rstrip('\r').split(','))
    return csvdata[-1][-2]

def send_sensor_data():
    mqtt_client.publish(co2_topic, str(readCO2.get_value(co2_reading_pin)))
    mqtt_client.publish(voc_topic, str(readVOC.get_value(VOC_outputA)))
    mqtt_client.publish(pm2_5_topic, str(readPM2_5.get_value()))
    mqtt_client.publish(temp_topic, str(readOnboardTemp.get_value()))
    
debounce_time = 0

def manual_data_read(pin):
    global debounce_time
    if (time.ticks_ms() - debounce_time > 750):
        print('Sending data from manual interrupt...')
        # TODO light up LED
        send_sensor_data()
        debounce_time = time.ticks_ms()
        print("Manual interrupt data successfully sent")

def button_interrupt_setup(pin):
    pin.irq(trigger=machine.Pin.IRQ_RISING, handler=manual_data_read)
# TODO light up LED while connecting
# TODO format into if __main__ blocks
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(securityInfo.ssid,securityInfo.wifi_password)

time_limit = 30
print("connecting to network {}...\nAuto timeout in 30 seconds".format(securityInfo.ssid))
while (not wlan.isconnected()):
    time.sleep(1)
    time_limit -= 1
    if time_limit == 0:
        raise ValueError("Could not connect to internet, ensure securityInfo properly updated")
print("Successfully connected to network")

# COPIED TOP, from https://core-electronics.com.au/guides/getting-started-with-mqtt-on-raspberry-pi-pico-w-connect-to-the-internet-of-things/

mqtt_host = "io.adafruit.com"
mqtt_username = securityInfo.mqtt_username
mqtt_password = securityInfo.mqtt_password

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "1s9U%18U8$#*1hN#Qusny2K@^Kz!C" # I used a random password generator for this

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()
print("Successfully connected to mqtt client, now starting main loop...")

try:
    co2_topic = securityInfo.co2_topic
    voc_topic = securityInfo.voc_topic
    pm2_5_topic = securityInfo.pm2_5_topic
    temp_topic = securityInfo.temp_topic
    # ozone_topic
    # inner_door_topic
    # outer_door_topic
    # water_level_topic
    
    
    interrupt_button_pin = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_DOWN)
    button_interrupt_setup(interrupt_button_pin)
    
    while True:
        
        co2_reading_pin, CO2_power = readCO2.setup_pins()
        VOC_power, VOC_outputA  = readVOC.setup_pins()

        # Publish the data to the topic!
        print('Auto Publishing data...')
        # TODO light up LED
        send_sensor_data()        
        print('Auto Publish finished')
        
        # Delay a bit to avoid hitting the rate limit, max rate is 20 per minute without premium
        # time.sleep(10)
        time.sleep(60*30) # delay for half an hour
except ImportError:
    raise ValueError("Failed to import collectSensorData, make sure it is copied onto board")
except KeyboardInterrupt:
    print("Successfully exited via keyboard")
finally:
    mqtt_client.disconnect()


# COPIED BOTTOM