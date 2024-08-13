#!/usr/bin/env python

"""
================================================
AB Electronics UK Expander Pi | RTC memory integer demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_rtcmemory_int.py
================================================

This demo shows how to write to and read from the internal battery
backed memory on the DS1307 RTC chip

"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

try:
    import ExpanderPi
except ImportError:
    print("Failed to import ExpanderPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        import ExpanderPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def int_to_array(val):
    """
    convert an integer into a four-byte array
    """
    array_bytes = [0, 0, 0, 0]
    array_bytes[3] = val & 0xFF
    val >>= 8
    array_bytes[2] = val & 0xFF
    val >>= 8
    array_bytes[1] = val & 0xFF
    val >>= 8
    array_bytes[0] = val & 0xFF
    return array_bytes


def array_to_int(array_bytes):
    """
    convert a four-byte array into an integer
    """
    val = (array_bytes[0] << 24) + (array_bytes[1] << 16) + \
          (array_bytes[2] << 8) + array_bytes[3]
    return val


def main():
    """
    Main program function
    """

    # create a new instance of the RTC class
    rtc = ExpanderPi.RTC()

    # integer to be written to the RTC memory
    write_value = 176247
    print("Writing to memory: ", write_value)

    # convert the integer into an array of bytes
    write_array = int_to_array(write_value)

    # write the array to the RTC memory
    rtc.write_memory(0x08, write_array)

    # read four bytes from the RTC memory into an array
    read_array = rtc.read_memory(0x08, 4)

    # combine the array values into an integer and print it
    print("Reading from memory: ", array_to_int(read_array))


if __name__ == "__main__":
    main()
