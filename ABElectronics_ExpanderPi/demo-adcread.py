#!/usr/bin/python

from ABElectronics_ExpanderPi import ADC
import time


# ================================================
# ABElectronics Expander Pi | ADC Read Demo
# Version 1.0 Created 21/08/2014
#
# run with: python demo-adcread.py
# ================================================

# this demo reads the voltage from channel 1 on the ADC inputs

adc = ADC() # create an instance of the ADC

adc.setADCrefvoltage(4.096) # set the reference voltage.  this should be set to the exact voltage measured on the Expander Pi Vref pin.

while True:
    print adc.readADCvoltage(1) # read the voltage from channel 1 and display on the screen
    time.sleep(0.5)

