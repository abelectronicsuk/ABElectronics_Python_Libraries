#!/usr/bin/env python

"""
================================================
AB Electronics UK: IO Zero 32 | Digital I/O Read Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This example reads from all 32 pins across both buses on the IO Zero 32.
The pullup or pulldown resistors may be needed on the inputs to stop them
from floating in an indeterminate state.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

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


def main():
    """
    Main program function
    """
    iobus1 = IOZero32(0x20)
    iobus2 = IOZero32(0x21)

    # We will read all inputs 1 to 16 from the I/O bus so 
    # set the inputs using the set_bus_direction method.
    iobus1.set_bus_direction(0xFFFF)

    # Repeat the steps above for the second bus
    iobus2.set_bus_direction(0xFFFF)

    while True:
        # Clear the console
        os.system("clear")

        # Read the pins 1 to 16 on both buses and print the results
        print("Bus 1                   Bus 2")
        print("Pin 1:  " + str(iobus1.read_pin(1)) +
              "               Pin 1:  " + str(iobus2.read_pin(1)))
        print("Pin 2:  " + str(iobus1.read_pin(2)) +
              "               Pin 2:  " + str(iobus2.read_pin(2)))
        print("Pin 3:  " + str(iobus1.read_pin(3)) +
              "               Pin 3:  " + str(iobus2.read_pin(3)))
        print("Pin 4:  " + str(iobus1.read_pin(4)) +
              "               Pin 4:  " + str(iobus2.read_pin(4)))
        print("Pin 5:  " + str(iobus1.read_pin(5)) +
              "               Pin 5:  " + str(iobus2.read_pin(5)))
        print("Pin 6:  " + str(iobus1.read_pin(6)) +
              "               Pin 6:  " + str(iobus2.read_pin(6)))
        print("Pin 7:  " + str(iobus1.read_pin(7)) +
              "               Pin 7:  " + str(iobus2.read_pin(7)))
        print("Pin 8:  " + str(iobus1.read_pin(8)) +
              "               Pin 8:  " + str(iobus2.read_pin(8)))
        print("Pin 9:  " + str(iobus1.read_pin(9)) +
              "               Pin 9:  " + str(iobus2.read_pin(9)))
        print("Pin 10: " + str(iobus1.read_pin(10)) +
              "               Pin 10: " + str(iobus2.read_pin(10)))
        print("Pin 11: " + str(iobus1.read_pin(11)) +
              "               Pin 11: " + str(iobus2.read_pin(11)))
        print("Pin 12: " + str(iobus1.read_pin(12)) +
              "               Pin 12: " + str(iobus2.read_pin(12)))
        print("Pin 13: " + str(iobus1.read_pin(13)) +
              "               Pin 13: " + str(iobus2.read_pin(13)))
        print("Pin 14: " + str(iobus1.read_pin(14)) +
              "               Pin 14: " + str(iobus2.read_pin(14)))
        print("Pin 15: " + str(iobus1.read_pin(15)) +
              "               Pin 15: " + str(iobus2.read_pin(15)))
        print("Pin 16: " + str(iobus1.read_pin(16)) +
              "               Pin 16: " + str(iobus2.read_pin(16)))

        # Wait 0.5 seconds before reading the pins again
        time.sleep(0.5)


if __name__ == "__main__":
    main()
