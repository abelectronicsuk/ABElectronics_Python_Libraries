#!/usr/bin/env python
"""
================================================
AB Electronics UK IO Pi | Digital I/O Read and Write Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iopireadwrite.py
================================================

This example reads pin 1 of bus 1 on the IO Pi board and sets
pin 1 of bus 2 to match.
The internal pull-up resistors are enabled so the input pin
will read as 1 unless the pin is connected to ground.

Initialise the IOPi device using the default addresses, you will need to
change the addresses if you have changed the jumpers on the IO Pi
"""
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time

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

    # create two instances of the IoPi class called io_bus1 and io_bus2 and set
    # the default i2c addresses
    io_bus1 = IOPi(0x20)  # bus 1 will be inputs
    io_bus2 = IOPi(0x21)  # bus 2 will be outputs

    # Each bus is divided into two 8-bit ports.  Port 0 controls pins 1 to 8,
    # Port 1 controls pins 9 to 16.
    # We will read the inputs on pin 1 of bus 1 so set port 0 as inputs and
    # enable the internal pull-up resistors
    io_bus1.set_port_direction(0, 0xFF)
    io_bus1.set_port_pullups(0, 0xFF)

    # We will write to the output pin 1 on bus 2 so set port 0 as outputs
    # and turn off the pins on port 0
    io_bus2.set_port_direction(0, 0x00)
    io_bus2.write_port(0, 0x00)

    while True:

        # Read pin 1 on bus 1.  If pin 1 is high set the output on
        # bus 2 pin 1 to high, otherwise set it to low.
        # Connect pin 1 on bus 1 to ground to see the output on
        # bus 2 pin 1 change state.
        if io_bus1.read_pin(1) == 1:

            io_bus2.write_pin(1, 1)
        else:
            io_bus2.write_pin(1, 0)

        # Wait 0.1 seconds before reading the pins again
        time.sleep(0.1)


if __name__ == "__main__":
    main()
