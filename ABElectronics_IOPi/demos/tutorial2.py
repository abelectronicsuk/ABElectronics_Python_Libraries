# ================================================
# ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1
# Version 1.1 Created 10/05/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python tutorial1.py
# ================================================

# This example uses the writePin and writePort methods to switch pin 1 on and off on the IO Pi.


#!/usr/bin/python 
from ABElectronics_IOPi import IOPI
import time

bus = IOPI(0x21)

bus.setPinDirection(1, 1) # set pin 1 as an input

bus.setPinDirection(8, 0) # set pin 8 as an output

bus.writePin(8,0) # turn off pin 8

bus.setPinPullup(1, 1) # enable the internal pull-up resistor on pin 1

bus.invertPin(1, 1) # invert pin 1 so a button press will register as 1



while True:
 
   if bus.readPin(1) == 1: # check to see if the button is pressed
      print 'button pressed' # print a message to the screen
      bus.writePin(8, 1) # turn on the led on pin 8
      time.sleep(2) # wait 2 seconds
   else:
      bus.writePin(8, 0) # turn off the led on pin 8
