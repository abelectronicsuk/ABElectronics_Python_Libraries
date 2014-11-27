#!/usr/bin/python

import smbus
import re

"""
================================================
ABElectronics Python Helper Functions
Version 1.0 Created 15/11/2014
Python 2 only
Requires python 2 smbus to be installed with: sudo apt-get install python-smbus
This file contains functions to load puthon smbus into an instance variable.
The bus object can then be used by multiple devices without conflicts.
================================================
"""


class ABEHelpers:

    def get_smbus(self):
        # detect i2C port number and assign to i2c_bus
        i2c_bus = 0
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
        return smbus.SMBus(i2c_bus)
