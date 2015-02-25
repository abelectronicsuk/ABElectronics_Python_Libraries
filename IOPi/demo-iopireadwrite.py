#!/usr/bin/python

from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time
import os

"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Read Write Demo
Version 1.0 Created 25/02/2015
Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: python demo-iopireadwrite.py
================================================

This example reads pin 1 of bus 1 on the IO Pi board and sets pin 1 of bus 2 to match.  
The internal pull-up resistors are enabled so the input pin will read as 1 unless
the pin is connected to ground. 

Initialise the IOPi device using the default addresses, you will need to
change the addresses if you have changed the jumpers on the IO Pi
"""
i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()

# create two instances of the IoPi class called bus1 and bus2 and set the default i2c addresses

bus1 = IoPi(i2c_bus, 0x20) # bus 1 will be inputs
bus2 = IoPi(i2c_bus, 0x21) # bus 2 will be outputs

# Each bus is divided up two 8 bit ports.  Port 0 controls pins 1 to 8, Port 1 controls pins 9 to 16.
# We will read the inputs on pin 1 of bus 1 so set port 0 to be inputs and
# enable the internal pull-up resistors
bus1.set_port_direction(0, 0xFF)
bus1.set_port_pullups(0, 0xFF)

# We will write to the output pin 1 on bus 2 so set port 0 to be outputs and
# turn off the pins on port 0
bus2.set_port_direction(0, 0x00)
bus2.write_port(0, 0x00)

while True:


    # read pin 1 on bus 1.  If pin 1 is high set the output on bus 2 pin 1 to high, otherwise set it to low.
    # connect pin 1 on bus 1 to ground to see the output on bus 2 pin 1 change state.
    if (bus1.read_pin(1) == 1):
    
        bus2.write_pin(1, 1)
    else:
        bus2.write_pin(1, 0)
                             
   

    # wait 0.1 seconds before reading the pins again
    time.sleep(0.1)
