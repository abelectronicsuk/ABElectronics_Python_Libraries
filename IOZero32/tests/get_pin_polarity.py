#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | test get_pin_polarity function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_pin_polarity.py
================================================

This test validates the get_pin_polarity function in the IOZero32 class.

=== Expected Result ============================

> Console Output:

get_pin_polarity() low boundary check: PASSED
get_pin_polarity() high boundary check: PASSED
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

    # Check get_pin_polarity for low out-of-bounds
    try:
        io_bus.get_pin_polarity(-1)
        pass
    except ValueError:
        print("get_pin_polarity() low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_pin_polarity() low boundary check: FAILED")
        pass

    # Check get_pin_polarity for low out-of-bounds
    try:
        io_bus.get_pin_polarity(17)
        pass
    except ValueError:
        print("get_pin_polarity() high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_pin_polarity() high boundary check: FAILED")
        pass

    for a in range(1, 17):
        io_bus.set_pin_polarity(a, 0)
        x = io_bus.get_pin_polarity(a)
        if x != 0:
            passed = False
            break
        io_bus.set_pin_polarity(a, 1)
        x = io_bus.get_pin_polarity(a)
        if x != 1:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
