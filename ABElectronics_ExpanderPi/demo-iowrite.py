#!/usr/bin/python

from ABElectronics_ExpanderPi import IO
import time

# ================================================
# ABElectronics Expander Pi | Digital I/O Interrupts Demo
# Version 1.0 Created 21/08/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python demo-iowrite.py
# ================================================

# This example uses the writePin and writeBank methods to switch the pins on and off on the I/O bus.

# Initialise the IO class and create an instance called io.
io = IO()

# We will write to the pins 9 to 16 so set port 1 to be outputs turn off the pins
io.setPortDirection(1, 0x00)
io.writePort(1, 0x00)

while True:
    
    # count to 255 and display the value on pins 9 to 16 in binary format
    for x in range(0,255):
        time.sleep(0.05)
        io.writePort(1, x) 

    #turn off all of the pins on bank 1
    io.writePort(1, 0x00)

    #now turn on all of the leds in turn by writing to one pin at a time
    io.writePin(9, 1)
    time.sleep(0.1)
    io.writePin(10, 1)
    time.sleep(0.1)
    io.writePin(11, 1)
    time.sleep(0.1)
    io.writePin(12, 1)
    time.sleep(0.1)
    io.writePin(13, 1)
    time.sleep(0.1)
    io.writePin(14, 1)
    time.sleep(0.1)
    io.writePin(15, 1)
    time.sleep(0.1)
    io.writePin(16, 1)

    #and turn off all of the leds in turn by writing to one pin at a time
    io.writePin(9, 0)
    time.sleep(0.1)
    io.writePin(10, 0)
    time.sleep(0.1)
    io.writePin(11, 0)
    time.sleep(0.1)
    io.writePin(12, 0)
    time.sleep(0.1)
    io.writePin(13, 0)
    time.sleep(0.1)
    io.writePin(14, 0)
    time.sleep(0.1)
    io.writePin(15, 0)
    time.sleep(0.1)
    io.writePin(16, 0)

    #repeat until the program ends