#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Pi Tests | write_pin

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 write_pin.py
================================================

This test validates the write_pin function in the IOPi class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

pin low boundary check: PASSED
pin high boundary check: PASSED
value low boundary check: PASSED
value high boundary check: PASSED
Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0xA0 0x02
W 0x20 0x12 0x00 0x00

W 0x20 0x12
R 0x20 0x12 0x00
W 0x20 0x12 0x01

looping to

W 0x20 0x12
R 0x20 0x12 0x7F
W 0x20 0x12 0xFF

W 0x20 0x13
R 0x20 0x13 0x00
W 0x20 0x13 0x01

looping to

W 0x20 0x13
R 0x20 0x13 0x7F
W 0x20 0x13 0xFF


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

    # Reset to 0x00
    iopi.write_bus(0x0000)

    # Check write_pin pin for low out-of-bounds
    try:
        iopi.write_pin(0, 0)
        pass
    except ValueError:
        print("pin low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("pin low boundary check: FAILED")
        pass

    # Check write_pin pin for high out-of-bounds
    try:
        iopi.write_pin(17, 0)
        pass
    except ValueError:
        print("pin high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("pin high boundary check: FAILED")
        pass

    # Check write_pin value for low out-of-bounds
    try:
        iopi.write_pin(0, -1)
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

    # Check write_pin value for high out-of-bounds
    try:
        iopi.write_pin(17, 2)
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

    for x in range(1, 17):
        iopi.write_pin(x, 1)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
