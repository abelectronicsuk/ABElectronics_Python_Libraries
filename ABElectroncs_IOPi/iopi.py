#!/usr/bin/python

from ABElectroncs_IOPi import IOPI
import time

# ================================================
# ABElectroncs IO Pi V2 32-Channel Port Expander
# Version 1.0 Created 01/02/2014
#
# Requires python smbus to be installed
# run with: sudo python iopi.py
# ================================================


# Initialise the IOPi device using the default address and cycle outputs in sequence.
# config IOPI(address(output/input, output/input) 
iopi = IOPI(0x20, True, False)


while True:
  
  for x in range(0,8):
   a = 1 << x
   iopi.setData(a,1)
   time.sleep(0.1)
   iopi.setData(0,1)
  for x in range(7,-1,-1):
    a = 1 << x
    iopi.setData(a,1)
    time.sleep(0.1)
    iopi.setData(0,1)    