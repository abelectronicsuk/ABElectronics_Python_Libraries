#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | test get_port_polarity function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_port_polarity.py
================================================

This test validates the get_port_polarity function in the IOPi class.

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
    from IOPi import IOPi
except ImportError:
    raise ImportError("Failed to import IOPi library")


def main():
    """
    Main program function
    """

    passed = True

    iopi = IOPi(0x20, False)  # new iopi object without initialisation

    # Check get_port_polarity for low out-of-bounds
    try:
        iopi.get_port_polarity(-1)
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
        iopi.get_port_polarity(2)
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
        iopi.invert_port(0, a)
        x = iopi.get_port_polarity(0)
        if x != a:
            passed = False
            break
        iopi.invert_port(1, a)
        x = iopi.get_port_polarity(1)
        if x != a:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
