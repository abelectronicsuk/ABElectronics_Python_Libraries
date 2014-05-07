#!/usr/bin/python

from ABElectronics_IOPi import IOPI
import time
import os

# ================================================
# ABElectronics IO Pi 32-Channel Port Expander - Input Read Demo
# Version 1.1 Created 30/04/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python iopiread.py
# ================================================

# This example reads the first 8 pins of bus 1 on the IO Pi board.  The internal pull-up resistors are enabled so each pin will read as 1 unless the pin is connected to ground.

# Initialise the IOPi device using the default addresses, you will need to change the addresses if you have changed the jumpers on the IO Pi
bus1 = IOPI(0x20)

# We will read the inputs 1 to 8 from bus 2 so set port 0 to be inputs and enable the internal pull-up resistors 
bus1.setPortDirection(0, 0xFF)
bus1.setPortPullups(0, 0xFF)

while True:
    # clear the console
    os.system('clear')

    # read the pins 1 to 8 and print the results
    print 'Pin 1: ' + str(bus1.readPin(1))
    print 'Pin 2: ' + str(bus1.readPin(2))
    print 'Pin 3: ' + str(bus1.readPin(3))
    print 'Pin 4: ' + str(bus1.readPin(4))
    print 'Pin 5: ' + str(bus1.readPin(5))
    print 'Pin 6: ' + str(bus1.readPin(6))
    print 'Pin 7: ' + str(bus1.readPin(7))
    print 'Pin 8: ' + str(bus1.readPin(8))
    
    # wait 0.5 seconds before reading the pins again
    time.sleep(0.1)