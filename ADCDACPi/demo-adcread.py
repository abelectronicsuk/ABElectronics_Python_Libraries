#!/usr/bin/python

from ABE_ADCDACPi import ADCDACPi
import time

"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | ADC Read Demo
Version 1.0 Created 17/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

run with: python demo-adcread.py
================================================

this demo reads the voltage from channel 1 on the ADC inputs
"""

adcdac = ADCDACPi(1)  # create an instance of the ADCDAC Pi with a DAC gain set to 1

# set the reference voltage.  this should be set to the exact voltage
# measured on the raspberry pi 3.3V rail.
adcdac.set_adc_refvoltage(3.3)

while True:
    # read the voltage from channel 1 and display on the screen
    print adcdac.read_adc_voltage(1)
    time.sleep(0.5)
