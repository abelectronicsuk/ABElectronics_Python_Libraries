#!/usr/bin/python

from ABElectroncs_IOPi import IOPI
import time

# ================================================
# ABElectroncs IO Pi V2 32-Channel Port Expander
# Version 1.0 Created 01/02/2014
#
# Requires python smbus to be installed
# run with: sudo python iopiread.py
# ================================================


# Initialise the IOPi device using the default addresses and set the output of bank 1 on IC1 to the input of bank 1 on IC2
# config IOPI(address(output/input, output/input) 
iopi = IOPI(0x20, True, True)
iopib = IOPI(0x21, False, False)

while True:
  activeinput = iopib.readData(1)
  iopi.setData(activeinput,1)
  iopi.setData(0,1)
  print(activeinput)