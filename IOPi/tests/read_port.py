#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | read_port

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 read_port.py
================================================

This test validates the read_port function in the IOPi class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

port low boundary check: PASSED
port high boundary check: PASSED
Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0xA0 0x02
W 0x20 0x12 0x00 0x00
W 0x20 0x00 0x00 0x00

W 0x20 0x12
R 0x20 0x00
W 0x20 0x13
R 0x20 0x00

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

try:
    import sys
    sys.path.append("..")
    from IOPi import IOPi
except ImportError:
    raise ImportError("Failed to import IOPi library")


def main():
    """
    Main program function
    """

    passed = True

    iopi = IOPi(0x20, False)  # new iopi object without initialisation

    # Reset to 0x00
    iopi.write_bus(0x0000)
    iopi.set_bus_direction(0xFFFF)

    # Check read_port port for low out-of-bounds
    try:
        iopi.read_port(-1)
        pass
    except ValueError:
        print("port low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("port low boundary check: FAILED")
        pass

    # Check read_port port for high out-of-bounds
    try:
        iopi.read_port(2)
        pass
    except ValueError:
        print("port high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("port high boundary check: FAILED")
        pass

    # Logic Analyser Check
    print("Logic output Started")

    iopi.read_port(0)
    iopi.read_port(1)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
