#!/usr/bin/python

from ABElectronics_ExpanderPi import RTC
import time

# ================================================
# ABElectronics Expander Pi |  Set Time Demo
# Version 1.0 Created 21/08/2014
#
# run with: python demo-rtcsetdate.py
# ================================================

# This demo shows how to set the time on the Expander Pi real-time clock and then read the current time at 1 second intervals

rtc = RTC() # create a new instance of the RTC class


rtc.setDate("2013-04-23T12:32:11") # set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS 

while True:
    print rtc.readDate() # read the date from the RTC in ISO 8601 format and print it to the screen
    time.sleep(1) # wait 1 second