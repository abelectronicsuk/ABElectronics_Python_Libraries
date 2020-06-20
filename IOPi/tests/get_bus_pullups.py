#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi Tests | test get_bus_pullups function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_bus_pullups.py
================================================

This test validates the get_bus_pullups function in the IOPi class.

=== Expected Result ============================

> Console Output:

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

    for a in range(1, 65536):
        iopi.set_bus_pullups(a)
        x = iopi.get_bus_pullups()
        if x != a:
            passed = False
            break
        iopi.set_bus_pullups(a)
        x = iopi.get_bus_pullups()
        if x != a:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
