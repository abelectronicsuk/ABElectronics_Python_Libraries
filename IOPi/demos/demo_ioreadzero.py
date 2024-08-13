#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Zero | Digital I/O Read Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioreadzero.py
================================================

This example reads from all 16 pins on the IO Pi Zero.
The internal pull-up resistors are enabled so each pin will read
as 1 unless the pin is connected to ground.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    io_bus = IOPi(0x20, True)

    # We will read the inputs 1 to 16 from the I/O bus so set Port 0 and
    # Port 1 as inputs and enable the internal pull-up resistors
    io_bus.set_port_direction(0, 0xFF)
    io_bus.set_port_pullups(0, 0xFF)

    io_bus.set_port_direction(1, 0xFF)
    io_bus.set_port_pullups(1, 0xFF)

    while True:
        # Clear the console
        os.system("clear")

        # Read the pins 1 to 16 and print the results
        print("Pin 1:  " + str(io_bus.read_pin(1)))
        print("Pin 2:  " + str(io_bus.read_pin(2)))
        print("Pin 3:  " + str(io_bus.read_pin(3)))
        print("Pin 4:  " + str(io_bus.read_pin(4)))
        print("Pin 5:  " + str(io_bus.read_pin(5)))
        print("Pin 6:  " + str(io_bus.read_pin(6)))
        print("Pin 7:  " + str(io_bus.read_pin(7)))
        print("Pin 8:  " + str(io_bus.read_pin(8)))
        print("Pin 9:  " + str(io_bus.read_pin(9)))
        print("Pin 10: " + str(io_bus.read_pin(10)))
        print("Pin 11: " + str(io_bus.read_pin(11)))
        print("Pin 12: " + str(io_bus.read_pin(12)))
        print("Pin 13: " + str(io_bus.read_pin(13)))
        print("Pin 14: " + str(io_bus.read_pin(14)))
        print("Pin 15: " + str(io_bus.read_pin(15)))
        print("Pin 16: " + str(io_bus.read_pin(16)))

        # Wait 0.1 seconds before reading the pins again
        time.sleep(0.1)


if __name__ == "__main__":
    main()
