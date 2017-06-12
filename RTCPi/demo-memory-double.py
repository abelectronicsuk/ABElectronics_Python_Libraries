#!/usr/bin/python

from ABE_RTCPi import RTC
from ABE_helpers import ABEHelpers
import struct

"""
================================================
ABElectronics RTC Pi real-time clock | RTC memory demo
Version 1.0 Created 03/01/2017


run with: python demo-memory-double.py
================================================

This demo shows how to write to and read from the internal battery 
backed memory on the DS1307 RTC chip
"""



def double_to_array(val):
    # convert a double into an eight byte array
    buf = bytearray(struct.pack('d', val))
    x = [0,0,0,0,0,0,0,0]
    for i in range(0, 8):
    	x[i] = buf[i]
    return x
    
    
def array_to_double(val):
    # convert an eight byte array into a double
    dval, = struct.unpack('d', bytearray(val))
    return (dval)


# create an instance of the helper class and create an i2c bus object
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()

# create a new instance of the RTC class
rtc = RTC(bus)

# number to be written to the RTC memory
value = 0.0005

# convert the number into an array of bytes
writearray = double_to_array(value)

# write the array to the RTC memory
rtc.write_memory(0x08, writearray)

# read eight bytes from the RTC memory into an array
read_array = rtc.read_memory(0x08, 8)

# combine the array values into an number and print it
print (array_to_double(read_array))