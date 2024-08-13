#!/usr/bin/env python

"""
================================================
AB Electronics UK RTC Pi | RTC memory double demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcmemory_double.py
================================================

This demo shows how to write to and read from the internal battery
backed memory on the DS1307 RTC chip
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import struct

try:
    from RTCPi import RTC
except ImportError:
    print("Failed to import RTCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from RTCPi import RTC
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def double_to_array(val):
    """
    Convert a double into an eight-byte array
    """
    buf = bytearray(struct.pack('d', val))
    array_bytes = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, 8):
        array_bytes[i] = buf[i]
    return array_bytes


def array_to_double(val):
    """
    Convert an eight-byte array into a double
    """
    double_value, = struct.unpack('d', bytearray(val))
    return double_value


def main():
    """
    Main program function
    """

    # Create a new instance of the RTC class
    rtc = RTC()

    # Number to be written to the RTC memory
    value = 0.0005
    print("Writing to memory: ", value)

    # Convert the number into an array of bytes
    write_array = double_to_array(value)

    # Write the array to the RTC memory
    rtc.write_memory(0x08, write_array)

    # Read eight bytes from the RTC memory into an array
    read_array = rtc.read_memory(0x08, 8)

    # Combine the array values into a number and print it
    print("Reading from memory: ", array_to_double(read_array))


if __name__ == "__main__":
    main()
