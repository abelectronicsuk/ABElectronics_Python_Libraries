#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers

"""
================================================
ABElectronics Servo Pi pwm controller | PWM servo controller demo
Version 1.0 18/11/2014 

run with: sudo python demo-servomove.py
================================================

This demo shows how to set the limits of movement on a servo 
and then move between those positions 

"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()

pwm = PWM(bus, 0x40)

# set the servo minimum, centre and maximum limits
servoMin = 250  # Min pulse length out of 4096
servoMed = 400  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096

# Set PWM frequency to 60 Hz
pwm.set_pwm_freq(60)
pwm.output_enable()

while (True):
    # Move servo on port 0 between three points
    pwm.set_pwm(0, 0, servoMin)
    time.sleep(0.5)
    pwm.set_pwm(0, 0, servoMed)
    time.sleep(0.5)
    pwm.set_pwm(0, 0, servoMax)
    time.sleep(0.5)
    # use set_all_pwm to set PWM on all outputs
