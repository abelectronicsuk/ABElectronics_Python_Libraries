#!/usr/bin/python

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC demo
Version 1.0 Created 09/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed
run with: python demo-read_voltage.py
================================================


Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
Sample rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCDifferentialPi(bus, 0x68, 0x69, 18)

while (True):

    # clear the console
    os.system('clear')

    # read from adc channels and print to screen
    print ("Channel 1: %d" % adc.read_raw(1))
    print ("Sign Bit: %d" % adc.get_signbit())
   

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
