#!/usr/bin/python
# -*- coding: utf-8 -*-

from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Pi HIH4000 humidity sensor demo
Version 1.0 Created 20/05/2015

Requires python smbus to be installed
run with: python demo-hih4000.py
================================================

The HIH4000 humidity sensor needs a load of at least 80K between the output
and ground pin so add a 100K resistor between the sensor output and the 
ADC Pi input pin to make the sensor work correctly

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

resistor_multiplier = 6.95225 # use 100K resistor in series with the input
zero_offset = 0.826 # zero offset value from calibration data printout
slope = 0.031483 # slope value from calibration data printout

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)





def calcHumidity(inval):
    voltage = inval * resistor_multiplier
    humidity = (voltage - zero_offset) / slope
    return humidity

while (True):

    # clear the console
    os.system('clear')

    # read from adc channels and print to screen
    print ("Humidity on channel 1: %0.1f%%" % calcHumidity(adc.read_voltage(1)))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
