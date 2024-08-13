#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | read_pin

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 read_pin.py
================================================

This test validates the read_pin function in the IOZero32 class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

pin low boundary check: PASSED
pin high boundary check: PASSED
Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0x02 0x00 0x00
W 0x20 0x06 0xFF 0xFF

W 0x20 0x00
R 0x20 0x00

looping 8 times

W 0x20 0x01
R 0x20 0x00

looping 8 times


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

    # Check read_pin pin for low out-of-bounds
    try:
        io_bus.read_pin(0)
        pass
    except ValueError:
        print("pin low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("pin low boundary check: FAILED")
        pass

    # Check read_pin pin for high out-of-bounds
    try:
        io_bus.read_pin(17)
        pass
    except ValueError:
        print("pin high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("pin high boundary check: FAILED")
        pass

    # Logic Analyser Check
    print("Logic output Started")

    for x in range(1, 17):
        io_bus.read_pin(x)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
