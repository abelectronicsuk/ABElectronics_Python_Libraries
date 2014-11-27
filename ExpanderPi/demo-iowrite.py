#!/usr/bin/python

from ABE_ExpanderPi import IO
from ABE_helpers import ABEHelpers
import time

"""
================================================
ABElectronics Expander Pi | Digital I/O Interrupts Demo
Version 1.0 Created 21/08/2014

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-iowrite.py
================================================

This example uses the write_pin and writeBank methods to switch the pins
on and off on the I/O bus.

Initialise the IO class and create an instance called io.
"""


i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
io = IO(bus)

# We will write to the pins 9 to 16 so set port 1 to be outputs turn off
# the pins
io.set_port_direction(1, 0x00)
io.write_port(1, 0x00)

while True:

    # count to 255 and display the value on pins 9 to 16 in binary format
    for x in range(0, 255):
        time.sleep(0.05)
        io.write_port(1, x)

    # turn off all of the pins on bank 1
    io.write_port(1, 0x00)

    # now turn on all of the leds in turn by writing to one pin at a time
    io.write_pin(9, 1)
    time.sleep(0.1)
    io.write_pin(10, 1)
    time.sleep(0.1)
    io.write_pin(11, 1)
    time.sleep(0.1)
    io.write_pin(12, 1)
    time.sleep(0.1)
    io.write_pin(13, 1)
    time.sleep(0.1)
    io.write_pin(14, 1)
    time.sleep(0.1)
    io.write_pin(15, 1)
    time.sleep(0.1)
    io.write_pin(16, 1)

    # and turn off all of the leds in turn by writing to one pin at a time
    io.write_pin(9, 0)
    time.sleep(0.1)
    io.write_pin(10, 0)
    time.sleep(0.1)
    io.write_pin(11, 0)
    time.sleep(0.1)
    io.write_pin(12, 0)
    time.sleep(0.1)
    io.write_pin(13, 0)
    time.sleep(0.1)
    io.write_pin(14, 0)
    time.sleep(0.1)
    io.write_pin(15, 0)
    time.sleep(0.1)
    io.write_pin(16, 0)

    # repeat until the program ends
