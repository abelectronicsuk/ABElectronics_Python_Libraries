#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi Tests | set_interrupt_defaults

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 set_interrupt_defaults.py
================================================

This test validates the set_interrupt_defaults function in the IOPi class.

Hardware Required: Logic Analyser on I2C Pins

=== Expected Result ============================

> Console Output:

port low boundary check: PASSED
port high boundary check: PASSED
value low boundary check: PASSED
value high boundary check: PASSED
Logic output Started
Logic output Ended

> Logic Analyser Output:

W 0x20 0xA0 0x02
W 0x20 0x06 0x00 0x00

W 0x20 0x06 0x00
W 0x20 0x07 0x00

looping to

W 0x20 0x06 0xFF
W 0x20 0x07 0xFF


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

    # Check set_interrupt_defaults port for low out of bounds
    try:
        iopi.set_interrupt_defaults(-1, 0)
        pass
    except ValueError:
        print("port low boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("port low boundary check: FAILED")
        pass

    # Check set_interrupt_defaults port for high out of bounds
    try:
        iopi.set_interrupt_defaults(2, 0)
        pass
    except ValueError:
        print("port high boundary check: PASSED")
        pass
    except IOError:
        passed = False
        print("I2C IOError")
    else:
        passed = False
        print("port high boundary check: FAILED")
        pass

    # Check set_interrupt_defaults value for low out of bounds
    try:
        iopi.set_interrupt_defaults(0, -1)
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

    # Check set_interrupt_defaults value for high out of bounds
    try:
        iopi.set_interrupt_defaults(0, 256)
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

    for x in range(0, 256):
        iopi.set_interrupt_defaults(0, x)
        iopi.set_interrupt_defaults(1, x)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
