#!/usr/bin/env python

"""
================================================
AB Electronics UK Expander Pi | Digital I/O Write Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iowrite.py
================================================

This example uses the write_pin and write_port methods to switch the pins
on and off on the I/O bus.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

try:
    import ExpanderPi
except ImportError:
    print("Failed to import ExpanderPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        import ExpanderPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    io_bus = ExpanderPi.IO()

    # We will write to the pins 9 to 16 so set port 1 as outputs and
    # turn off the pins
    io_bus.set_port_direction(1, 0x00)
    io_bus.write_port(1, 0x00)

    while True:

        # count to 255 and display the value on pins 9 to 16 in binary format
        for val in range(0, 255):
            time.sleep(0.05)
            io_bus.write_port(1, val)

        # turn off all the pins on bank 1
        io_bus.write_port(1, 0x00)

        # now turn on all the LEDs in turn by writing to one pin at a time
        io_bus.write_pin(9, 1)
        time.sleep(0.1)
        io_bus.write_pin(10, 1)
        time.sleep(0.1)
        io_bus.write_pin(11, 1)
        time.sleep(0.1)
        io_bus.write_pin(12, 1)
        time.sleep(0.1)
        io_bus.write_pin(13, 1)
        time.sleep(0.1)
        io_bus.write_pin(14, 1)
        time.sleep(0.1)
        io_bus.write_pin(15, 1)
        time.sleep(0.1)
        io_bus.write_pin(16, 1)

        # and turn off all the LEDs in turn by writing to one pin at a time
        io_bus.write_pin(9, 0)
        time.sleep(0.1)
        io_bus.write_pin(10, 0)
        time.sleep(0.1)
        io_bus.write_pin(11, 0)
        time.sleep(0.1)
        io_bus.write_pin(12, 0)
        time.sleep(0.1)
        io_bus.write_pin(13, 0)
        time.sleep(0.1)
        io_bus.write_pin(14, 0)
        time.sleep(0.1)
        io_bus.write_pin(15, 0)
        time.sleep(0.1)
        io_bus.write_pin(16, 0)

        # repeat until the program ends


if __name__ == "__main__":
    main()
