#!/usr/bin/python

from ABE_ExpanderPi import DAC
import time

"""
================================================
ABElectronics Expander Pi | DAC Write Demo
Version 1.0 Created 21/08/2014
Version 1.1 Updated 11/06/2017 updated to include changes to Expander Pi library

run with: python demo-dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz on channel 1
"""

dac = DAC(1) # create a dac instance with  the gain set to 1

while True:
    dac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
    time.sleep(1)  # wait 1 seconds
    dac.set_dac_voltage(1, 0)  # set the voltage on channel 1 to 0V
    time.sleep(1)  # wait 1 seconds
