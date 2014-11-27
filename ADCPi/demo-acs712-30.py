#!/usr/bin/python

from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Pi ACS712 30 Amp current sensor demo
Version 1.0 Created 15/07/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed
run with: python demo-acs712-30.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 12)

# change the 2.5 value to be half of the supply voltage.


def calcCurrent(inval):
    return ((inval) - 2.5) / 0.066

while (True):

    # clear the console
    os.system('clear')

    # read from adc channels and print to screen
    print ("Current on channel 1: %02f" % calcCurrent(adc.read_voltage(1)))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
