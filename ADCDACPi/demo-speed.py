#!/usr/bin/python3

from ABE_ADCDACPi import ADCDACPi
import time
import datetime
import numpy as N
"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | ADC Read Speed Demo
Version 1.0 Created 17/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Version 1.2 21/04/2017 added code to save value into a numpy array and calculate the speed
run with: python demo-speed.py
================================================
this demo reads the voltage from channel 1 on the ADC inputs
"""

adcdac = ADCDACPi(1)  # create an instance of the ADCDAC Pi with a DAC gain set to 1

# set the reference voltage.  this should be set to the exact voltage
# measured on the raspberry pi 3.3V rail.
adcdac.set_adc_refvoltage(3.3)

counter = 1
totalsamples = 100000

a = N.zeros(totalsamples)

starttime = datetime.datetime.now()
print ("Start: " + str(starttime))

while (counter < totalsamples):
    # read the voltage from channel 1 and display on the screen
    a[counter] = adcdac.read_adc_voltage(1,0)

    counter = counter + 1

endtime = datetime.datetime.now()

print ("End: " + str(endtime))
totalseconds = (endtime - starttime).total_seconds()

samplespersecond = totalsamples / totalseconds

print (str(samplespersecond) + " samples per second")
