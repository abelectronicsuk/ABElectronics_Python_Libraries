#!/usr/bin/python
import datetime
import re

"""
================================================
ABElectronics RTC Pi Real-time clock
Version 1.0 Created 01/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Requires python smbus to be installed with: sudo apt-get install python-smbus

================================================
"""


class RTC:
    # Define registers values from datasheet
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYOFWEEK = 0x03
    DAY = 0x04
    MONTH = 0x05
    YEAR = 0x06
    CONTROL = 0x07

    # variables
    __rtcAddress = 0x68  # I2C address
    # initial configuration - square wave and output disabled, frequency set
    # to 32.768KHz.
    __config = 0x03
    # the DS1307 does not store the current century so that has to be added on
    # manually.
    __century = 2000

    global _bus

    # local methods

    def __init__(self, bus):
        self._bus = bus
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def __bcd_to_dec(self, x):
        return x - 6 * (x >> 4)

    def __dec_to_bcd(self, val):
        return ((val / 10 * 16) + (val % 10))

    def __get_century(self, val):
        if len(val) > 2:
            y = val[0] + val[1]
            self.__century = int(y) * 100
        return

    def __updatebyte(self, byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """

        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    # public methods
    def set_date(self, date):
        """
        set the date and time on the RTC
        date must be in ISO 8601 format - YYYY-MM-DDTHH:MM:SS
        """

        d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        self.__get_century(date)
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.SECONDS,
            self.__dec_to_bcd(
                d.second))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.MINUTES,
            self.__dec_to_bcd(
                d.minute))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.HOURS,
            self.__dec_to_bcd(
                d.hour))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.DAYOFWEEK,
            self.__dec_to_bcd(
                d.weekday()))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.DAY,
            self.__dec_to_bcd(
                d.day))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.MONTH,
            self.__dec_to_bcd(
                d.month))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.YEAR,
            self.__dec_to_bcd(
                d.year -
                self.__century))
        return

    def read_date(self):
        """
        read the date and time from the RTC in ISO 8601 format -
        YYYY-MM-DDTHH:MM:SS
        """

        seconds, minutes, hours, dayofweek, day, month,\
            year = self._bus.read_i2c_block_data(self.__rtcAddress, 0, 7)
        date = (
            "%02d-%02d-%02dT%02d:%02d:%02d " %
            (self.__bcd_to_dec(year) +
             self.__century,
             self.__bcd_to_dec(month),
             self.__bcd_to_dec(day),
             self.__bcd_to_dec(hours),
             self.__bcd_to_dec(minutes),
             self.__bcd_to_dec(seconds)))
        return date

    def enable_output(self):
        """
        Enable the output pin
        """

        self.__config = self.__updatebyte(self.__config, 7, 1)
        self.__config = self.__updatebyte(self.__config, 4, 1)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__config = self.__updatebyte(self.__config, 7, 0)
        self.__config = self.__updatebyte(self.__config, 4, 0)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def set_frequency(self, frequency):
        """
        set the frequency of the output pin square-wave
        options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        """

        if frequency == 1:
            self.__config = self.__updatebyte(self.__config, 0, 0)
            self.__config = self.__updatebyte(self.__config, 1, 0)
        if frequency == 2:
            self.__config = self.__updatebyte(self.__config, 0, 1)
            self.__config = self.__updatebyte(self.__config, 1, 0)
        if frequency == 3:
            self.__config = self.__updatebyte(self.__config, 0, 0)
            self.__config = self.__updatebyte(self.__config, 1, 1)
        if frequency == 4:
            self.__config = self.__updatebyte(self.__config, 0, 1)
            self.__config = self.__updatebyte(self.__config, 1, 1)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return
    
    def write_memory(self, address, valuearray):
    	"""
    	write to the memory on the ds1307
    	the ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes
    	variables are:
    	address: 0x08 to 0x3F
    	valuearray: byte array containing data to be written to memory
    	"""
    	
    	if address >= 0x08 and address <= 0x3F:
    	    if address + len(valuearray) <= 0x3F:
    	        self._bus.write_i2c_block_data(self.__rtcAddress, address, valuearray)
    	    else:
    	        print 'memory overflow error: address + length exceeds 0x3F'
    	else:
    	    print 'address out of range'
    	    
    	    
    def read_memory(self, address, length):
    	"""
    	read from the memory on the ds1307
    	the ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes
    	variables are:
    	address: 0x08 to 0x3F
    	length: up to 32 bytes.  length can not exceed the avaiable address space.
    	"""
    	
    	if address >= 0x08 and address <= 0x3F:
    	    if address <= (0x3F - length):
    	        return self._bus.read_i2c_block_data(self.__rtcAddress, address, length)
    	    else:
    	        print 'memory overflow error: address + length exceeds 0x3F'
    	else:
    	    print 'address out of range'
    	