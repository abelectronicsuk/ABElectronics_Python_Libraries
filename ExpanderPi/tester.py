#!/usr/bin/python
from ABE_ExpanderPi import RTC
from ABE_ExpanderPi import ADC
from ABE_ExpanderPi import IO
from ABE_ExpanderPi import DAC
import time
import os

# ================================================
# ABElectronics Expander Pi |  Tester
# Version 1.0 Created 08/11/2014
# Version 1.1 Updated 11/06/2017 updated to include changes to Expander Pi library
#
# run with: python tester.py
# ================================================

# This script tests the various functionality of the Expander Pi

rtc = RTC()  # create a new instance of the RTC class
adc = ADC()  # create an instance of the ADC class
io = IO()  # create an instance of the IO class
dac = DAC(1)  # create an instance of the DAC class with a gain of 0

# set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS
rtc.set_date("2017-01-01T00:00:00")
dac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
dac.set_dac_voltage(2, 1.0)  # set the voltage on channel 2 to 1.0V

# set the reference voltage.  this should be set to the exact voltage
# measured on the Expander Pi Vref pin.
adc.set_adc_refvoltage(4.096)

while True:
    # clear the console
    os.system('clear')

    # read the date from the RTC in ISO 8601 format and print it to the screen
    print 'Date: ' + rtc.read_date()
    print ''
    print 'ADC: '
    print 'Channel 1: ' + str(adc.read_adc_voltage(1, 0))
    print 'Channel 2: ' + str(adc.read_adc_voltage(2, 0))
    print 'Channel 3: ' + str(adc.read_adc_voltage(3, 0))
    print 'Channel 4: ' + str(adc.read_adc_voltage(4, 0))
    print 'Channel 5: ' + str(adc.read_adc_voltage(5, 0))
    print 'Channel 6: ' + str(adc.read_adc_voltage(6, 0))
    print 'Channel 7: ' + str(adc.read_adc_voltage(7, 0))
    print 'Channel 8: ' + str(adc.read_adc_voltage(8, 0))
    print ''
    print 'IO: '
    print 'Pin 1: ' + str(io.read_pin(1))
    print 'Pin 2: ' + str(io.read_pin(2))
    print 'Pin 3: ' + str(io.read_pin(3))
    print 'Pin 4: ' + str(io.read_pin(4))
    print 'Pin 5: ' + str(io.read_pin(5))
    print 'Pin 6: ' + str(io.read_pin(6))
    print 'Pin 7: ' + str(io.read_pin(7))
    print 'Pin 8: ' + str(io.read_pin(8))
    time.sleep(0.2)
