#!/usr/bin/python

from ABElectronics_ADCPi import ADCPi
import time
import os

# ================================================
# ABElectronics ADC Pi 8-Channel ADC demo
# Version 1.0 Created 09/05/2014
#
# Requires python smbus to be installed
# run with: python demo-readvoltage.py
# ================================================


# Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
# Sample rate can be 12,14, 16 or 18
adc = ADCPi(0x68, 0x69, 12)

while (True):

  # clear the console
  os.system('clear')

  # read from adc channels and print to screen
  print ("Channel 1: %02f" % adc.readVoltage(1))
  print ("Channel 2: %02f" % adc.readVoltage(2))
  print ("Channel 3: %02f" % adc.readVoltage(3))
  print ("Channel 4: %02f" % adc.readVoltage(4))
  print ("Channel 5: %02f" % adc.readVoltage(5))
  print ("Channel 6: %02f" % adc.readVoltage(6))
  print ("Channel 7: %02f" % adc.readVoltage(7))
  print ("Channel 8: %02f" % adc.readVoltage(8))

 
  # wait 0.5 seconds before reading the pins again
  time.sleep(0.5)