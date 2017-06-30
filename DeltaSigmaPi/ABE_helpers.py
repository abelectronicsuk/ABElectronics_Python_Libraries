#!/usr/bin/python
try:
    import smbus
except ImportError:
    raise ImportError("python-smbus not found. Install with 'sudo apt-get install python-smbus'")
import re
import os

"""
================================================
ABElectronics Python Helper Functions
Version 1.3 Created 30/06/2017
Python 2 only
Requires python 2 smbus to be installed with: sudo apt-get install python-smbus
This file contains functions to load puthon smbus into an instance variable.
The bus object can then be used by multiple devices without conflicts.
================================================
"""


class ABEHelpers:

    def get_smbus(self):
        i2c_bus = 1
        # detect the device that is being used
        device = os.uname()[1]

        if (device == "orangepione"): # running on orange pi one
            i2c_bus = 0

        elif (device == "orangepiplus"): # running on orange pi one
            i2c_bus = 0

        elif (device == "linaro-alip"): # running on Asus Tinker Board
            i2c_bus = 1

        elif (device == "raspberrypi"): # running on raspberry pi

            # detect i2C port number and assign to i2c_bus

            for line in open('/proc/cpuinfo').readlines():
                m = re.match('(.*?)\s*:\s*(.*)', line)
                if m:
                    (name, value) = (m.group(1), m.group(2))
                    if name == "Revision":
                        if value[-4:] in ('0002', '0003'):
                            i2c_bus = 0
                        else:
                            i2c_bus = 1
                        break
        try:
            return smbus.SMBus(i2c_bus)
        except IOError:
            print("Could not open the i2c bus.")
            print("Please check that i2c is enabled and python-smbus and i2c-tools are installed.")
            print("For more information please visit:")
            print("https://www.abelectronics.co.uk/kb/article/1/i2c--smbus-and-raspbian-linux")
