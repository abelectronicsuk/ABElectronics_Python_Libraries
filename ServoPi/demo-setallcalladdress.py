#!/usr/bin/python

from ABE_ServoPi import PWM
import time
from ABE_helpers import ABEHelpers

"""
================================================
ABElectronics Servo Pi pwm controller | PWM all call i2c address demo
Version 1.0 19/01/2015

run with: sudo python demo-setallcalladdress.py
================================================

This demo shows how to set the I2C address for the All Call function
All Call allows you to control several Servo Pi boards simultaneously on the same I2C address
"""

# create an instance of the ABEHelpers class and use it 
# to find the correct i2c bus
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()

# create an instance of the PWM class on i2c address 0x40
pwm = PWM(bus, 0x40)

# Set the all call address to 0x30
pwm.set_allcall_address(0x30)

# Disable the all call address 
#pwm.disable_allcall_address()

# Enable the all call address 
#pwm.enable_allcall_address()