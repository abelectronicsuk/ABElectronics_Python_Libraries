#!/usr/bin/python

from ABE_ADCDACPi import ADCDACPi
import time
import RPi.GPIO as GPIO

"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | DAC Write Demo
Version 1.0 Created 17/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
run with: python demo-dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz
"""

# The ADCDAC Pi uses GPIO pin 22 to control the DAC.  
# This will need to be turned off for the DAC to operate correctly.

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, False)

adcdac = ADCDACPi(1) # create an instance of the ADCDAC Pi with a DAC gain set to 1

while True:
    adcdac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
    time.sleep(0.5)  # wait 0.5 seconds
    adcdac.set_dac_voltage(1, 0)  # set the voltage on channel 1 to 0V
    time.sleep(0.5)  # wait 0.5 seconds
