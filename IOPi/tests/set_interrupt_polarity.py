#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | set_interrupt_polarity

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 set_interrupt_polarity.py
================================================

This test validates the set_interrupt_polarity function in the IOPi class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

value low boundary check: PASSED
value high boundary check: PASSED
Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0xA0 0x02

W 0x20 0xA0 0x00
W 0x20 0xA0 0x02


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

    # Check set_interrupt_polarity value for low out-of-bounds
    try:
        iopi.set_interrupt_polarity(-1)
        pass
    except ValueError:
        print("value low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("value low boundary check: FAILED")
        pass

    # Check set_interrupt_polarity value for high out-of-bounds
    try:
        iopi.set_interrupt_polarity(2)
        pass
    except ValueError:
        print("value high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("value high boundary check: FAILED")
        pass

    # Logic Analyser Check
    print("Logic output Started")

    iopi.set_interrupt_polarity(0)
    iopi.set_interrupt_polarity(1)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
