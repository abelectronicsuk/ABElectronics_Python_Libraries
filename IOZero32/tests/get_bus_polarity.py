#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | test get_bus_polarity function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_bus_polarity.py
================================================

This test validates the get_bus_polarity function in the IOZero32 class.

=== Expected Result ============================

> Console Output:

Test Passed

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
from sys import stdout

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

    for a in range(1, 65536):
        stdout.write("\r%d" % a)
        stdout.flush()
        iobus.set_bus_polarity(a)
        x = iobus.get_bus_polarity()
        if x != a:
            passed = False
            break       

    stdout.write("\n")
    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
