#!/usr/bin/python

from ABElectronics_ExpanderPi import RTC
from ABElectronics_ExpanderPi import ADC
from ABElectronics_ExpanderPi import IO
from ABElectronics_ExpanderPi import DAC
import time
import os

# ================================================
# ABElectronics Expander Pi |  Tester
# Version 1.0 Created 08/11/2014
#
# run with: python tester.py
# ================================================

# This script tests the various functionality of the Expander Pi

rtc = RTC() # create a new instance of the RTC class
adc = ADC() # create an instance of the ADC class
io = IO() # create an instance of the IO class
dac = DAC() # create an instance of the DAC class

rtc.setDate("2014-01-01T00:00:00") # set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS 
dac.setDACvoltage(1, 1.5) # set the voltage on channel 1 to 1.5V
dac.setDACvoltage(2, 1.0) # set the voltage on channel 2 to 1.0V

adc.setADCrefvoltage(4.096) # set the reference voltage.  this should be set to the exact voltage measured on the Expander Pi Vref pin.

while True:
    # clear the console
    os.system('clear')

    print 'Date: ' +  rtc.readDate() # read the date from the RTC in ISO 8601 format and print it to the screen
    print ''
    print 'ADC: '
    print 'Channel 1: ' + str(adc.readADCvoltage(1))
    print 'Channel 2: ' + str(adc.readADCvoltage(2))
    print 'Channel 3: ' + str(adc.readADCvoltage(3))
    print 'Channel 4: ' + str(adc.readADCvoltage(4))
    print 'Channel 5: ' + str(adc.readADCvoltage(5))
    print 'Channel 6: ' + str(adc.readADCvoltage(6))
    print 'Channel 7: ' + str(adc.readADCvoltage(7))
    print 'Channel 8: ' + str(adc.readADCvoltage(8))
    print ''
    print 'IO: '
    print 'Pin 1: ' + str(io.readPin(1))
    print 'Pin 2: ' + str(io.readPin(2))
    print 'Pin 3: ' + str(io.readPin(3))
    print 'Pin 4: ' + str(io.readPin(4))
    print 'Pin 5: ' + str(io.readPin(5))
    print 'Pin 6: ' + str(io.readPin(6))
    print 'Pin 7: ' + str(io.readPin(7))
    print 'Pin 8: ' + str(io.readPin(8))
    time.sleep(0.2)