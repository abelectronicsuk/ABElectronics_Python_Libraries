#!/usr/bin/python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1
Version 1.1 Created 10/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed: sudo apt-get install python-smbus
run with: sudo python tutorial1.py
================================================

This example uses the write_pin and write_port methods to switch pin 1 on
and off on the IO Pi.
"""
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time

i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()

bus = IoPi(i2c_bus, 0x21)

bus.set_port_direction(0, 0x00)
bus.write_port(0, 0x00)

while True:
    bus.write_pin(1, 1)
    time.sleep(1)
    bus.write_pin(1, 0)
    time.sleep(1)
