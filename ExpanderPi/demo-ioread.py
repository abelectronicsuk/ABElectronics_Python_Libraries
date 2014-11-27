#!/usr/bin/python

from ABE_ExpanderPi import IO
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics Expander Pi | Digital I/O Interrupts Demo
Version 1.0 Created 21/08/2014

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-ioread.py
================================================

This example reads the first 8 pins of on the Expander Pi Digital I/O
port.  The internal pull-up resistors are enabled so each pin will read
as 1 unless the pin is connected to ground.

Initialise the IO class and create an instance called io.
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
io = IO(bus)

# We will read the inputs 1 to 8 from the I/O bus so set port 0 to be
# inputs and enable the internal pull-up resistors
io.set_port_direction(0, 0xFF)
io.set_port_pullups(0, 0xFF)

while True:
    # clear the console
    os.system('clear')

    # read the pins 1 to 8 and print the results
    print 'Pin 1: ' + str(io.read_pin(1))
    print 'Pin 2: ' + str(io.read_pin(2))
    print 'Pin 3: ' + str(io.read_pin(3))
    print 'Pin 4: ' + str(io.read_pin(4))
    print 'Pin 5: ' + str(io.read_pin(5))
    print 'Pin 6: ' + str(io.read_pin(6))
    print 'Pin 7: ' + str(io.read_pin(7))
    print 'Pin 8: ' + str(io.read_pin(8))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.1)
