#!/usr/bin/python

from ABE_ExpanderPi import ADC
import time

"""
================================================
ABElectronics Expander Pi | ADC Read Demo
Version 1.0 Created 21/08/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Version 1.2 11/06/2017 updated to include changes to Expander Pi library

run with: python demo-adcread.py
================================================

this demo reads the voltage from channel 1 on the ADC inputs
"""


adc = ADC()  # create an instance of the ADC

# set the reference voltage.  this should be set to the exact voltage
# measured on the Expander Pi Vref pin.
adc.set_adc_refvoltage(4.096)

while True:
    # read the voltage from channel 1 in single ended mode and display on the screen
    print adc.read_adc_voltage(1,0)
    time.sleep(0.5)
