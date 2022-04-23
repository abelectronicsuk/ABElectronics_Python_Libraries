#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | test get_pin_direction function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_pin_direction.py
================================================

This test validates the get_pin_direction function in the IOZero32 class.

=== Expected Result ============================

> Console Output:

get_pin_direction() low boundary check: PASSED
get_pin_direction() high boundary check: PASSED
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

    iobus = IOZero32(0x20)  # new iobus object

    # Check get_pin_direction for low out of bounds
    try:
        iobus.get_pin_direction(-1)
        pass
    except ValueError:
        print("get_pin_direction() low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_pin_direction() low boundary check: FAILED")
        pass

    # Check get_pin_direction for low out of bounds
    try:
        iobus.get_pin_direction(17)
        pass
    except ValueError:
        print("get_pin_direction() high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_pin_direction() high boundary check: FAILED")
        pass

    for a in range(1, 17):
        iobus.set_pin_direction(a, 0)
        x = iobus.get_pin_direction(a)
        if x != 0:
            passed = False
            break
        iobus.set_pin_direction(a, 1)
        x = iobus.get_pin_direction(a)
        if x != 1:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
