#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | test get_port_polarity function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_port_polarity.py
================================================

This test validates the get_port_polarity function in the IOZero32 class.

=== Expected Result ============================

> Console Output:

get_port_polarity() low boundary check: PASSED
get_port_polarity() high boundary check: PASSED
Test Passed

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

    io_bus = IOZero32(0x20)  # new io_bus object

    # Check get_port_polarity for low out-of-bounds
    try:
        io_bus.get_port_polarity(-1)
        pass
    except ValueError:
        print("get_port_polarity() low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_port_polarity() low boundary check: FAILED")
        pass

    # Check get_port_polarity for low out-of-bounds
    try:
        io_bus.get_port_polarity(2)
        pass
    except ValueError:
        print("get_port_polarity() high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_port_polarity() high boundary check: FAILED")
        pass

    for a in range(1, 256):
        io_bus.set_port_polarity(0, a)
        x = io_bus.get_port_polarity(0)
        if x != a:
            passed = False
            break
        io_bus.set_port_polarity(1, a)
        x = io_bus.get_port_polarity(1)
        if x != a:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
