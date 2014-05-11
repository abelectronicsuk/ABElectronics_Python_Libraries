# ================================================
# ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1a
# Version 1.1 Created 10/05/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python tutorial1a.py
# ================================================

# This example uses the writePort method to count in binary using 8 LEDs


#!/usr/bin/python 
from ABElectronics_IOPi import IOPI
import time

bus = IOPI(0x21)

bus.setPortDirection(0, 0x00)
bus.writePort(0, 0x00)

while True:
   for x in range(0,255):      
      bus.writePort(0, x) 
      time.sleep(0.5)
	
      bus.writePort(0, 0x00)
