#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | __init__

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 IOZero32_init.py
================================================

This test validates the __init__ function in the IOZero32 class.

=== Expected Result ============================

> Console Output:

I2C address low boundary check: PASSED
I2C address high boundary check: PASSED
Test Passed

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

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

    # Check i2c address for low out-of-bounds
    try:
        a = IOZero32(0x19)
        del a
        pass
    except ValueError:
        print("I2C address low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C address low boundary check: FAILED")
    else:
        passed = False
        print("I2C address low boundary check: FAILED")
        pass

    # Check i2c address for high out-of-bounds
    try:
        b = IOZero32(0x28)
        del b
        pass
    except ValueError:
        print("I2C address high boundary check: PASSED")
        pass
    else:
        passed = False
        print("I2C address high boundary check: FAILED")
        pass


    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
