#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | test get_pin_direction function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_pin_direction.py
================================================

This test validates the get_pin_direction function in the IOPi class.

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
    from IOPi import IOPi
except ImportError:
    raise ImportError("Failed to import IOPi library")


def main():
    """
    Main program function
    """

    passed = True

    iopi = IOPi(0x20, False)  # new iopi object without initialisation

    # Check get_pin_direction for low out-of-bounds
    try:
        iopi.get_pin_direction(-1)
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

    # Check get_pin_direction for low out-of-bounds
    try:
        iopi.get_pin_direction(17)
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
        iopi.set_pin_direction(a, 0)
        x = iopi.get_pin_direction(a)
        if x != 0:
            passed = False
            break
        iopi.set_pin_direction(a, 1)
        x = iopi.get_pin_direction(a)
        if x != 1:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
