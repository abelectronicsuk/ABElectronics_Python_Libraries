#!/usr/bin/python

from ABE_RTCPi import RTC
from ABE_helpers import ABEHelpers
import time

"""
================================================
ABElectronics RTC Pi real-time clock | RTC clock output demo
Version 1.0 Created 19/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

run with: python demo-rtcout.py
================================================

This demo shows how to enable the clock square wave output on the RTC Pi
and set the frequency
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)  # create a new instance of the RTC class


# set the frequency of the output square-wave, options are: 1 = 1Hz, 2 =
# 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
rtc.set_frequency(3)
rtc.enable_output()  # enable the square-wave
