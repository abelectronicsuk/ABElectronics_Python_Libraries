#!/usr/bin/python

from ABElectronics_RTCPi import RTC
import time

# ================================================
# ABElectronics RTC Pi real-time clock | RTC clock output demo
# Version 1.0 Created 19/05/2014
#
# run with: python demo-rtcout.py
# ================================================

# This demo shows how to enable the clock square wave output on the RTC Pi and set the frequency 

rtc = RTC() # create a new instance of the RTC class


rtc.setFrequency(3)# set the frequency of the output square-wave, options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
rtc.enableOutput() # enable the square-wave 

