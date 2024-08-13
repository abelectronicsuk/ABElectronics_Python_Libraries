#!/usr/bin/env python

"""
================================================
AB Electronics UK IO Zero 32 Tests | set_port_direction

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python3 set_port_direction.py
================================================

This test validates the set_port_direction function in the IOZero32 class.

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

W 0x20 0x06 0x00
W 0x20 0x07 0x00

looping to

W 0x20 0x06 0xFF
W 0x20 0x07 0xFF


"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

try:
    from IOZero32 import IOZero32
except ImportError:
    try:
        import sys
        sys.path.append("..")
        from IOZero32 import IOZero32
    except ImportError:
        raise ImportError(
            "Failed to import IOZero32 library")


def main():
    """
    Main program function
    """

    passed = True

    io_bus = IOZero32(0x20)  # new io_bus object

    # Check set_port_direction port for low out-of-bounds
    try:
        io_bus.set_port_direction(-1, 0)
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

    # Check set_port_direction port for high out-of-bounds
    try:
        io_bus.set_port_direction(2, 0)
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

    # Check set_port_direction value for low out-of-bounds
    try:
        io_bus.set_port_direction(0, -1)
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

    # Check set_port_direction value for high out-of-bounds
    try:
        io_bus.set_port_direction(0, 256)
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
        io_bus.set_port_direction(0, x)
        io_bus.set_port_direction(1, x)

    print("Logic output Ended")

    if passed is False:
        print("Test Failed")


if __name__ == "__main__":
    main()
