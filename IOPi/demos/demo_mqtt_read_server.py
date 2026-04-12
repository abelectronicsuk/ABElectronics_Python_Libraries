#!/usr/bin/env python3
"""
================================================
AB Electronics UK IO Pi 32-Channel Port Expander - MQTT Server Read Demo
Requires python smbus & mosquitto to be installed

Install smbus: sudo apt-get install python3-smbus
Install mosquitto: sudo apt-get install mosquitto
Install paho-mqtt: sudo apt-get install python3-paho-mqtt

Run with: python3 demo_mqtt_read_server.py
================================================
This example uses MQTT to communicate with a Raspberry Pi and IO Pi Plus
to read the pins on the IO Pi.
Initialises the IOPi device using the default addresses
"""

import time
import paho.mqtt.client as mqtt

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys

        sys.path.append('..')
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

# Setup IOPi I2C addresses            
io_bus1 = IOPi(0x20)
io_bus2 = IOPi(0x21)

# We will read the inputs 1 to 16 from the I/O bus so set port 0 and
# port 1 as inputs and enable the internal pull-up resistors
io_bus1.set_port_direction(0, 0xFF)
io_bus1.set_port_pullups(0, 0xFF)

io_bus1.set_port_direction(1, 0xFF)
io_bus1.set_port_pullups(1, 0xFF)

# Repeat the steps above for the second bus
io_bus2.set_port_direction(0, 0xFF)
io_bus2.set_port_pullups(0, 0xFF)

io_bus2.set_port_direction(1, 0xFF)
io_bus2.set_port_pullups(1, 0xFF)


# MQTT section ------------------------


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected: {reason_code}")
    client.subscribe("sensor/iopi/ports")


def on_message(client, userdata, msg):
    # called when receiving an MQTT message
    message = str(msg.payload)
    print(msg.topic + " " + message)


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))


# setup client
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# client.username_pw_set("your_username", "your_password") # uncomment if your mqtt broker uses authentication
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.0.0.50", 1883, 60)
client.loop_start()

while True:
    sensor_data = [io_bus1.read_port(0), io_bus1.read_port(1), io_bus2.read_port(0), io_bus2.read_port(1)]
    client.publish("sensor/iopi/ports", str(sensor_data))
    time.sleep(10)
