#!/usr/bin/python

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import time
import os
import math

"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC read Resistance thermometer 
using a Wheatstone bridge.
This demo uses a Semitec NTC (Negative Temperature Coefficient) Thermistors
10kohm 1%, Manufacturer Part No: 103AT-11

Purchased from Mouser Electronics, Part No: 954-103AT-11

The circuit is connected to the + and - inputs on channel 7 on the 
ADC Differential Pi. This can also be used on the Delta Sigma Pi

The Wheatstone bridge is comprised of three 10K resistors and the 
Resistance thermometer

Version 1.0 Created 30/10/2015

Requires python smbus to be installed
run with: python demo-resistance-thermometer.py
================================================


    
Initialise the ADC device using the default addresses and 18 bit sample rate, 
change this value if you have changed the address selection jumpers
Bit rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCDifferentialPi(bus, 0x68, 0x69, 18)

# the resistor values for the Wheatstone bridge are:
resistor1 = 10000
resistor2 = 10000
resistor3 = 10000
# Input voltage
voltin = 3.3
# Resistance thermometer values from datasheet
bResistance = 3435
t25Resistance = 10000

# Constants
t0 = 273.15;
t25 = t0 + 25;

def calcResistance(voltage):
    return (resistor2*resistor3 + resistor3* (resistor1+resistor2)*voltage / voltin )/ (resistor1- (resistor1+resistor2)*voltage / voltin)

def calcTemp(resistance):
    return 1 / ( (math.log(resistance / t25Resistance) / bResistance) + (1 / t25) ) - t0;

# loop forever reading the values and printing them to screen
while (True):
    # read from adc channels and print to screen
   
    bridgeVoltage =  adc.read_voltage(1)
    thermresistance = calcResistance(bridgeVoltage)
    temperature = calcTemp(thermresistance)
    
    # clear the console
    os.system('clear')
    # print values to screen
    
    print ("Bridge Voltage: %02f volts" % bridgeVoltage)
    print ("Resistance: %d ohms" % thermresistance)
    print ("Temperature: %.2fC" % temperature)
    
	
   

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)