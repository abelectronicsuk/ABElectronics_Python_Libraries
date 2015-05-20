#!/usr/bin/python
# -*- coding: utf-8 -*-

from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Pi TMP36 temperature sensor demo
Version 1.0 Created 20/05/2015

Requires python smbus to be installed
run with: python demo-tmp36.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)



def calcTemperature(inval):
    # TMP36 returns 0.01 volts per C - -40C to +125C
    # 750mV = 25C and 500mV = 0C so the temperature is (voltage / 0.01) - 50

    return ((inval/0.01)-50)

while (True):

    # clear the console
    os.system('clear')

    # read from adc channels and print to screen
    print ("Temperature on channel 1: %0.02f°C" % calcTemperature(adc.read_voltage(1)))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
