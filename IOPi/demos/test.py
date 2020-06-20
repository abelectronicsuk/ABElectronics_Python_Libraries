#!/usr/bin/env python

"""
================================================
ABElectronics Expander Pi | Digital I/O Read Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This example reads the first 8 pins of on the Expander Pi Digital I/O
port.  The internal pull-up resistors are enabled so each pin will read
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
    '''
    Main program function
    '''
    iobus = IOPi(0x20, False)

    # We will read the inputs 1 to 16 from the I/O bus so set port 0,
    # port 1 to be inputs and enable the internal pull-up resistors
    iobus.set_port_direction(0, 0xA1)
    print("Port direction 0: " + hex(iobus.get_port_direction(0)))

    iobus.set_port_direction(1, 0xB1)
    print("Port direction 1: " + hex(iobus.get_port_direction(1)))

    iobus.set_port_pullups(0, 0xC1)
    print("Port pullups 0: " + hex(iobus.get_port_pullups(0)))

    iobus.set_port_pullups(1, 0xD1)
    print("Port pullups 1: " + hex(iobus.get_port_pullups(1)))

    iobus.invert_port(0, 0xE1)
    print("Invert Port 0: " + hex(iobus.get_port_polarity(0)))

    iobus.invert_port(1, 0xF1)
    print("Invert Port 1: " + hex(iobus.get_port_polarity(1)))


if __name__ == "__main__":
    main()
