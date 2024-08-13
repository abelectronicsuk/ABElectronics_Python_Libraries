#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | read_bus

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 read_bus.py
================================================

This test validates the read_bus function in the IOZero32 class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0x02 0x00 0x00
W 0x20 0x06 0xFF 0xFF

W 0x20 0x00
R 0x20 0x00 0x00

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

try:
    import sys
    sys.path.append("..")
    from IOZero32 import IOZero32
except ImportError:
    raise ImportError("Failed to import IOZero32 library")


def main():
    """
    Main program function
    """

    passed = True

    io_bus = IOZero32(0x20)  # new io_bus object without initialisation

    # Reset to 0x00
    io_bus.write_bus(0x0000)
    io_bus.set_bus_direction(0xFFFF)
    
    # Logic Analyser Check
    print("Logic output Started")

    io_bus.read_bus()

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
