#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | test get_interrupt_on_port function

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 get_interrupt_on_port.py
================================================

This test validates the get_interrupt_on_port function in the IOPi class.

=== Expected Result ============================

> Console Output:

get_interrupt_on_port() low boundary check: PASSED
get_interrupt_on_port() high boundary check: PASSED
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

    # Check get_interrupt_on_port for low out-of-bounds
    try:
        iopi.get_interrupt_on_port(-1)
        pass
    except ValueError:
        print("get_interrupt_on_port() low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_interrupt_on_port() low boundary check: FAILED")
        pass

    # Check get_interrupt_on_port for low out-of-bounds
    try:
        iopi.get_interrupt_on_port(2)
        pass
    except ValueError:
        print("get_interrupt_on_port() high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("get_interrupt_on_port() high boundary check: FAILED")
        pass

    for a in range(1, 256):
        iopi.set_interrupt_on_port(0, a)
        x = iopi.get_interrupt_on_port(0)
        if x != a:
            passed = False
            break
        iopi.set_interrupt_on_port(1, a)
        x = iopi.get_interrupt_on_port(1)
        if x != a:
            passed = False
            break

    if passed is False:
        print("Test Failed")
    else:
        print("Test Passed")


if __name__ == "__main__":
    main()
