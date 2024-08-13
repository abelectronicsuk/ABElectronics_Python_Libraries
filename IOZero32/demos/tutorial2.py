#!/usr/bin/env python

"""
================================================
AB Electronics UK: IO Zero 32 | Tutorial 2

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This tutorial uses a button to control an LED.  For the full tutorial visit
https://www.abelectronics.co.uk/kb/article/1100/io-zero-32-tutorial-2---push-the-button

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
try:
    from IOZero32 import IOZero32
except ImportError:
    print("Failed to import IOZero32 from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOZero32 import IOZero32
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

import time

bus = IOZero32(0x20)
bus.set_pin_direction(1, 1)  # Set pin 1 as an input
bus.set_pin_direction(8, 0)  # Set pin 8 as an output
bus.write_pin(8, 0)  # turn off pin 8

while True:
    if bus.read_pin(1) == 1:  # Check to see if the button is pressed
        print("button pressed")  # Print a message to the screen
        bus.write_pin(8, 1)  # Turn on the LED on pin 8
        time.sleep(2)  # Wait 2 seconds
    else:
        bus.write_pin(8, 0)  # Turn off the LED on pin 8
