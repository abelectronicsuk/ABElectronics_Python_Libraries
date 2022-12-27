#!/usr/bin/env python

"""
================================================
AB Electronics UK RTC Pi | RTC memory integer demo

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


def int_to_array(val):
    '''
    Convert an integer into a four-byte array
    '''
    arraybytes = [0, 0, 0, 0]
    arraybytes[3] = val & 0xFF
    val >>= 8
    arraybytes[2] = val & 0xFF
    val >>= 8
    arraybytes[1] = val & 0xFF
    val >>= 8
    arraybytes[0] = val & 0xFF
    return arraybytes


def array_to_int(arraybytes):
    '''
    Convert a four-byte array into an integer
    '''
    val = (arraybytes[0] << 24) + (arraybytes[1] << 16) + \
          (arraybytes[2] << 8) + arraybytes[3]
    return val


def main():
    '''
    Main program function
    '''

    # Create a new instance of the RTC class
    rtc = RTC()

    # Integer to be written to the RTC memory
    writeval = 176247
    print("Writing to memory: ", writeval)

    # Convert the integer into an array of bytes
    writearray = int_to_array(writeval)

    # Write the array to the RTC memory
    rtc.write_memory(0x08, writearray)

    # Read four bytes from the RTC memory into an array
    readarray = rtc.read_memory(0x08, 4)

    # Combine the array values into an integer and print it
    print("Reading from memory: ", array_to_int(readarray))

if __name__ == "__main__":
    main()
