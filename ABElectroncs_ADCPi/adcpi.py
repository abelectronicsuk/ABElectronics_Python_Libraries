#!/usr/bin/python

from ABElectroncs_ADCPi import ADC


# ================================================
# ABElectroncs ADC Pi V2 8-Channel ADC demo
# Version 1.0 Created 01/02/2014
#
# Requires python smbus to be installed
# run with: sudo python adcpi.py
# ================================================


# Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
# Sample rate can be 12, 16 or 18
adc = ADC(0x68, 0x69, 18)

while (True):
  # read from adc channel and print to screen
  adc.changechannel(1)
  print ("Channel 1: %02f" % adc.getadcreading(1))
  adc.changechannel(2)
  print ("Channel 2: %02f" % adc.getadcreading(2))
  adc.changechannel(3)
  print ("Channel 3: %02f" % adc.getadcreading(3))
  adc.changechannel(4)
  print ("Channel 4: %02f" % adc.getadcreading(4))
  adc.changechannel(5)
  print ("Channel 5: %02f" % adc.getadcreading(5))
  adc.changechannel(6)
  print ("Channel 6: %02f" % adc.getadcreading(6))
  adc.changechannel(7)
  print ("Channel 7: %02f" % adc.getadcreading(7))
  adc.changechannel(8)
  print ("Channel 8: %02f" % adc.getadcreading(8))