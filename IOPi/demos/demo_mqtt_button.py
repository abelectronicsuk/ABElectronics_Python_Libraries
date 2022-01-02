#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi | MQTT I/O Button Read Demo

Requires python smbus to be installed
For Python 3 install with: sudo apt-get install python3-smbus

Requires paho-mqtt library to be installed
sudo apt-get install python3-pip
sudo pip3 install paho-mqtt

run with: python demo_mqtt_button.py
================================================

This example reads a button press from Pin 1 on Bus 1 of the IO Pi 
and publishes it to an MQTT broker.

The internal pull-up resistor on pin 1 is enabled so the pin will read
as 1 unless the pin is connected to ground.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
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

def on_disconnect(client, userdata, rc):
    print("MQTT Disconnected with result code " + str(rc))

def main():

    iobus = IOPi(0x20)
    iobus.set_pin_direction(1, 1) # set pin 1 as an input
    iobus.set_pin_pullup(1, 1) # enable the 100K pull-up resistor
    
    # MQTT connection parameters
    mqtt_broker = '192.168.0.1'
    mqtt_user = 'user'
    mqtt_pass = 'password'
    mqtt_port = 1883
    
    # Create an MQTT client instance
    client = mqtt.Client("P1") #create new instance
    client.username_pw_set(mqtt_user, mqtt_pass)
    client.on_disconnect = on_disconnect
    
    previous_state = 0 # stores the previous button state

    while(True):
        button_state = iobus.read_pin(1) # read the value from pin 1

        if button_state != previous_state: # check for a change the button state
            previous_state = button_state
            print("Button state changed to " + str(button_state))

            # connect to the MQTT broker and publish a message
            client.connect(mqtt_broker, mqtt_port, 60)
            client.publish("/iopi/button1" ,str(button_state))
            client.disconnect()
        
        time.sleep(0.1) # wait 100ms to debounce switch

if __name__ == "__main__":
    main()