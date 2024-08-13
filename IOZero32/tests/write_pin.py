#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | write_pin

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 write_pin.py
================================================

This test validates the write_pin function in the IOZero32 class.

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

W 0x20 0x02
R 0x20 0x02 0x00
W 0x20 0x02 0x01

looping to

W 0x20 0x02
R 0x20 0x02 0x7F
W 0x20 0x02 0xFF

W 0x20 0x03
R 0x20 0x03 0x00
W 0x20 0x03 0x01

looping to

W 0x20 0x03
R 0x20 0x03 0x7F
W 0x20 0x03 0xFF


"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

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

    io_bus = IOZero32(0x20)  # new io_bus object

    # Reset to 0x00
    io_bus.write_bus(0x0000)

    # Check write_pin pin for low out-of-bounds
    try:
        io_bus.write_pin(0, 0)
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
        io_bus.write_pin(17, 0)
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
        io_bus.write_pin(0, -1)
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
        io_bus.write_pin(17, 2)
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
        io_bus.write_pin(x, 1)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
