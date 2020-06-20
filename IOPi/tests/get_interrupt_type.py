#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi Tests | test get_interrupt_type function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_interrupt_type.py
================================================

This test validates the get_interrupt_type function in the IOPi class.

=== Expected Result ============================

> Console Output:

get_interrupt_type() low boundary check: PASSED
get_interrupt_type() high boundary check: PASSED
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

    # Check get_interrupt_type for low out of bounds
    try:
        iopi.get_interrupt_type(-1)
        pass
    except ValueError:
        print("get_interrupt_type() low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_interrupt_type() low boundary check: FAILED")
        pass

    # Check get_interrupt_type for low out of bounds
    try:
        iopi.get_interrupt_type(2)
        pass
    except ValueError:
        print("get_interrupt_type() high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_interrupt_type() high boundary check: FAILED")
        pass

    for a in range(1, 256):
        iopi.set_interrupt_type(0, a)
        x = iopi.get_interrupt_type(0)
        if x != a:
            passed = False
            break
        iopi.set_interrupt_type(1, a)
        x = iopi.get_interrupt_type(1)
        if x != a:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
