#!/usr/bin/python

from ABE_ADCPi import ADCPi
from ABE_helpers import ABEHelpers
import datetime
import time

"""
================================================
ABElectronics ADC Pi 8-Channel ADC data-logger demo
Version 1.0 Created 11/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed
run with: python demo-read_voltage.py
================================================

Initialise the ADC device using the default addresses and sample rate, change
this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""


i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)


def writetofile(texttowrtite):
    f = open('adclog.txt', 'a')
    f.write(str(datetime.datetime.now()) + " " + texttowrtite)
    f.closed

while (True):

    # read from adc channels and write to the log file
    writetofile("Channel 1: %02f\n" % adc.read_voltage(1))
    writetofile("Channel 2: %02f\n" % adc.read_voltage(2))
    writetofile("Channel 3: %02f\n" % adc.read_voltage(3))
    writetofile("Channel 4: %02f\n" % adc.read_voltage(4))
    writetofile("Channel 5: %02f\n" % adc.read_voltage(5))
    writetofile("Channel 6: %02f\n" % adc.read_voltage(6))
    writetofile("Channel 7: %02f\n" % adc.read_voltage(7))
    writetofile("Channel 8: %02f\n" % adc.read_voltage(8))

    # wait 1 second before reading the pins again
    time.sleep(1)
