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

bus.setPortDirection(0, 0x00)
bus.writePort(0, 0x00)

while True:
	bus.writePin(1, 1)
	time.sleep(1)
	bus.writePin(1, 0)
	time.sleep(1)
