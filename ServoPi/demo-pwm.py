#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers

"""
================================================
ABElectronics Servo Pi pwm controller | PWM output demo
Version 1.0 18/11/2014 

run with: sudo python demo-pwm.py
================================================

This demo shows how to set a 1KHz output frequency and change the pulse width 
between the minimum and maximum values
"""

# create an instance of the ABEHelpers class and use it 
# to find the correct i2c bus
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()

# create an instance of the PWM class on i2c address 0x40
pwm = PWM(bus, 0x40)

# Set PWM frequency to 1 Khz and enable the output
pwm.set_pwm_freq(1000)
pwm.output_enable()

while (True):
    for x in range(1, 4095, 5):        
        pwm.set_pwm(0, 0, x)
        #time.sleep(0.01)
    for x in range(4095, 1, -5):
        pwm.set_pwm(0, 0, x)
        #time.sleep(0.01)
