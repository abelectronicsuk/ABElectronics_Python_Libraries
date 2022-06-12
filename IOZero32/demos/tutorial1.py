#!/usr/bin/env python

"""
================================================
AB Electronics UK: IO Zero 32 | Tutorial 1

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This tutorial controls 8 leds connected to bus 1.  For the full tutorial visit
https://www.abelectronics.co.uk/kb/article/1099/io-zero-32-tutorial-1---the-blinking-led

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
bus.set_port_direction(0, 0x00)
bus.write_port(0, 0x00)
while True:
    bus.write_pin(1, 1)
    time.sleep(1)
    bus.write_pin(1, 0)
    time.sleep(1)