#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi Tests | __init__

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 IOPi_init.py
================================================

This test validates the __init__ function in the IOPi class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

I2C address low boundary check: PASSED
I2C address high boundary check: PASSED
I2C initialise boundary check: PASSED
Object created without initialisation
Object created with initialisation

> Logic Analyser Output:

W 0x20 0xA0 0x02

10ms delay

W 0x20 0xA0 0x02
W 0x20 0x00 0xFF 0xFF
W 0x20 0x0C 0x00 0x00
W 0x20 0x02 0x00 0x00

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

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

    # Check i2c address for low out of bounds
    try:
        a = IOPi(0x19)
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

    # Check i2c address for high out of bounds
    try:
        b = IOPi(0x28)
        del b
        pass
    except ValueError:
        print("I2C address high boundary check: PASSED")
        pass
    else:
        passed = False
        print("I2C address high boundary check: FAILED")
        pass

    # Check initialise parameter for out of bounds
    try:
        b = IOPi(0x20, 42)
        del b
        pass
    except ValueError:
        print("I2C initialise boundary check: PASSED")
        pass
    else:
        passed = False
        print("I2C initialise boundary check: FAILED")
        pass

    # Logic analyser test

    print("Object created without initialisation")
    c = IOPi(0x20, False)
    del c

    time.sleep(0.01)  # sleep 10ms

    print("Object created with initialisation")
    d = IOPi(0x20, True)
    del d

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
