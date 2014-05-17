#!/usr/bin/python

from ABElectronics_ADCDACPi import ADCDACPi
import time


# ================================================
# ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | ADC Read Demo
# Version 1.0 Created 17/05/2014
#
# run with: python demo-adcread.py
# ================================================

# this demo reads the voltage from channel 2 on the ADC inputs

adcdac = ADCDACPi() # create an instance of ADCDACPi

adcdac.setADCrefvoltage(3.3) # set the reference voltage.  this should be set to the exact voltage measured on the raspberry pi 3.3V rail.

while True:
    print adcdac.readADCvoltage(2) # read the voltage from channel 2 and display on the screen
    time.sleep(0.5)

