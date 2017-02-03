#!/usr/bin/python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Output Write Demo
Version 1.1 Created 30/04/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-iopiwrite.py
================================================

This example uses the write_pin and writeBank methods to switch the pins
on and off on the IO Pi.

Initialise the IOPi device using the default addresses, you will need to
change the addresses if you have changed the jumpers on the IO Pi
"""
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time
i2c_helper = ABEHelpers()
newbus = i2c_helper.get_smbus()

bus1 = IoPi(newbus, 0x20)

# We will write to the pins 9 to 16 from bus 1 so set port 1 to be outputs
# turn off the pins
bus1.set_port_direction(1, 0x00)
bus1.write_port(1, 0x00)

while True:

    # count to 255 and display the value on pins 9 to 16 in binary format
    for x in range(0, 255):
        time.sleep(0.05)
        bus1.write_port(1, x)

    # turn off all of the pins on bank 1
    bus1.write_port(1, 0x00)

    # now turn on all of the leds in turn by writing to one pin at a time
    bus1.write_pin(9, 1)
    time.sleep(0.1)
    bus1.write_pin(10, 1)
    time.sleep(0.1)
    bus1.write_pin(11, 1)
    time.sleep(0.1)
    bus1.write_pin(12, 1)
    time.sleep(0.1)
    bus1.write_pin(13, 1)
    time.sleep(0.1)
    bus1.write_pin(14, 1)
    time.sleep(0.1)
    bus1.write_pin(15, 1)
    time.sleep(0.1)
    bus1.write_pin(16, 1)

    # and turn off all of the leds in turn by writing to one pin at a time
    bus1.write_pin(9, 0)
    time.sleep(0.1)
    bus1.write_pin(10, 0)
    time.sleep(0.1)
    bus1.write_pin(11, 0)
    time.sleep(0.1)
    bus1.write_pin(12, 0)
    time.sleep(0.1)
    bus1.write_pin(13, 0)
    time.sleep(0.1)
    bus1.write_pin(14, 0)
    time.sleep(0.1)
    bus1.write_pin(15, 0)
    time.sleep(0.1)
    bus1.write_pin(16, 0)

    # repeat until the program ends
