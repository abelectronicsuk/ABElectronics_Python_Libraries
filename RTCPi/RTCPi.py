#!/usr/bin/env python
"""
================================================
AB Electronics UK RTC Pi Real-time clock

Requires smbus2 or python smbus to be installed
================================================
"""
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python3-smbus or smbus2 not found")
import re
import platform
import datetime


class RTC:
    """
    Based on the Maxim DS1307
    """

    # Define registers from the datasheet
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYOFWEEK = 0x03
    DAY = 0x04
    MONTH = 0x05
    YEAR = 0x06
    CONTROL = 0x07

    # Variables
    __rtc_address = 0x68  # I2C address
    # Initial configuration - square wave and output disabled, frequency set
    # to 32.768KHz.
    __rtc_config = 0x03
    # The DS1307 does not store the current century so that has to be 
    # added on manually.
    __century = 2000

    __bus = None

    # Local methods

    @staticmethod
    def __get_smbus(bus):
        """
        Internal method for getting an instance of the I2C bus

        :param bus: I2C bus number.  If the value is None the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int
        :return: I2C bus for the target device
        :rtype: SMBus
        :raises IOError: Could not open the I2C bus
        """
        i2c_bus = 1
        if bus is not None:
            i2c_bus = bus
        else:
            # detect the device that is being used
            device = platform.uname()[1]

            if device == "orangepione":  # orange pi one
                i2c_bus = 0

            elif device == "orangepizero2":  # orange pi zero 2
                i2c_bus = 3

            elif device == "orangepiplus":  # orange pi plus
                i2c_bus = 0

            elif device == "orangepipcplus":  # orange pi pc plus
                i2c_bus = 0

            elif device == "linaro-alip":  # Asus Tinker Board
                i2c_bus = 1

            elif device == "bpi-m2z":  # Banana Pi BPI M2 Zero Ubuntu
                i2c_bus = 0

            elif device == "bpi-iot-ros-ai":  # Banana Pi BPI M2 Zero Raspbian
                i2c_bus = 0

            elif device == "raspberrypi":  # running on raspberry pi
                # detect I2C port number and assign to i2c_bus
                for line in open('/proc/cpuinfo').readlines():
                    model = re.match('(.*?)\\s*:\\s*(.*)', line)
                    if model:
                        (name, value) = (model.group(1), model.group(2))
                        if name == "Revision":
                            if value[-4:] in ('0002', '0003'):
                                i2c_bus = 0  # original model A or B
                            else:
                                i2c_bus = 1  # later models
                            break
        try:
            return SMBus(i2c_bus)
        except IOError:
            raise 'Could not open the I2C bus'

    @staticmethod
    def __update_byte(byte, bit, value):
        """
        Internal method for setting the value of a single bit within a byte

        :param byte: input value
        :type byte: int
        :param bit: location to update
        :type bit: int
        :param value: new bit, 0 or 1
        :type value: int
        :return: updated value
        :rtype: int
        """

        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    @staticmethod
    def __bcd_dec(bcd):
        """
        Internal method for converting a BCD format number to decimal

        :param bcd: BCD formatted number
        :type bcd: int
        :return: decimal number
        :rtype: int
        """
        return bcd - 6 * (bcd >> 4)

    @staticmethod
    def __dec_bcd(dec):
        """
        Internal method for converting a decimal format number to BCD

        :param dec: decimal number
        :type dec: int
        :return: BCD formatted number
        :rtype: int
        """
        bcd = 0
        for value_a in (dec // 10, dec % 10):
            for value_b in (8, 4, 2, 1):
                if value_a >= value_b:
                    bcd += 1
                    value_a -= value_b
                bcd <<= 1
        return bcd >> 1

    def __get_century(self, val):
        """
        Internal method for storing the current century

        :param val: year
        :type val: string
        """
        if len(val) > 2:
            year = val[0] + val[1]
            self.__century = int(year) * 100
        return

    # public methods

    def __init__(self, bus=None):
        """
        Initialise the RTC module
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int, optional
        """
        self.__bus = self.__get_smbus(bus)
        self.__bus.write_byte_data(self.__rtc_address, self.CONTROL,
                                   self.__rtc_config)
        return

    def set_date(self, date):
        """
        Set the date and time on the RTC

        :param date: ISO 8601 formatted string - "YYYY-MM-DDTHH:MM:SS"
        :type date: string
        """
        new_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        self.__get_century(date)
        write_value = [self.__dec_bcd(new_date.second),
                       self.__dec_bcd(new_date.minute),
                       self.__dec_bcd(new_date.hour),
                       self.__dec_bcd(new_date.weekday()),
                       self.__dec_bcd(new_date.day),
                       self.__dec_bcd(new_date.month),
                       self.__dec_bcd(new_date.year - self.__century)]

        self.__bus.write_i2c_block_data(self.__rtc_address, 0x00, write_value)

        return

    def read_date(self):
        """
        Read the date and time from the RTC

        :return: ISO 8601 formatted string - "YYYY-MM-DDTHH:MM:SS"
        :rtype: string
        """
        read_value = self.__bus.read_i2c_block_data(self.__rtc_address, 0, 7)
        date = ("%02d-%02d-%02dT%02d:%02d:%02d" % (self.__bcd_dec(read_value[6]) +
                                                   self.__century,
                                                   self.__bcd_dec(read_value[5]),
                                                   self.__bcd_dec(read_value[4]),
                                                   self.__bcd_dec(read_value[2]),
                                                   self.__bcd_dec(read_value[1]),
                                                   self.__bcd_dec(read_value[0])))
        return date

    def enable_output(self):
        """
        Enable the output pin
        """

        self.__rtc_config = self.__update_byte(self.__rtc_config, 7, 1)
        self.__rtc_config = self.__update_byte(self.__rtc_config, 4, 1)
        self.__bus.write_byte_data(
            self.__rtc_address, self.CONTROL, self.__rtc_config)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__rtc_config = self.__update_byte(self.__rtc_config, 7, 0)
        self.__rtc_config = self.__update_byte(self.__rtc_config, 4, 0)
        self.__bus.write_byte_data(
            self.__rtc_address, self.CONTROL, self.__rtc_config)
        return

    def set_frequency(self, frequency):
        """
        Set the frequency of the output pin square-wave

        :param frequency: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        :type frequency: int
        """

        if frequency == 1:
            self.__rtc_config = self.__update_byte(self.__rtc_config, 0, 0)
            self.__rtc_config = self.__update_byte(self.__rtc_config, 1, 0)
        if frequency == 2:
            self.__rtc_config = self.__update_byte(self.__rtc_config, 0, 1)
            self.__rtc_config = self.__update_byte(self.__rtc_config, 1, 0)
        if frequency == 3:
            self.__rtc_config = self.__update_byte(self.__rtc_config, 0, 0)
            self.__rtc_config = self.__update_byte(self.__rtc_config, 1, 1)
        if frequency == 4:
            self.__rtc_config = self.__update_byte(self.__rtc_config, 0, 1)
            self.__rtc_config = self.__update_byte(self.__rtc_config, 1, 1)
        self.__bus.write_byte_data(
            self.__rtc_address, self.CONTROL, self.__rtc_config)
        return

    def write_memory(self, address, valuearray):
        """
        Write to the memory on the DS1307
        The DS1307 contains 56-Byte, battery-backed RAM with Unlimited Writes

        :param address: 0x08 to 0x3F
        :type address: int
        :param valuearray: byte array containing data to be written to memory
        :type valuearray: int array
        :raises ValueError: write_memory: memory overflow error,
                            address length exceeds 0x3F
        :raises ValueError: write_memory: address out of range
        """

        if 0x08 <= address <= 0x3F:
            if address + len(valuearray) <= 0x3F:
                self.__bus.write_i2c_block_data(
                    self.__rtc_address, address, valuearray)
            else:
                raise ValueError('write_memory: memory overflow error: address + \
                                length exceeds 0x3F')
        else:
            raise ValueError('write_memory: address out of range')

    def read_memory(self, address, length):
        """
        Read from the memory on the DS1307
        The DS1307 contains 56-Byte, battery-backed RAM with Unlimited Writes

        :param address: 0x08 to 0x3F
        :type address: int
        :param length: number of bytes to read, up to 32 bytes.
                       length can not exceed the address space.
        :type length: int
        :raises ValueError: read_memory: memory overflow error,
                            address length exceeds 0x3F
        :raises ValueError: read_memory: address out of range
        :return: array of bytes from RAM
        :rtype: int array
        """

        if 0x08 <= address <= 0x3F:
            if address <= (0x3F - length):
                return self.__bus.read_i2c_block_data(self.__rtc_address,
                                                      address, length)
            else:
                raise ValueError('read_memory: memory overflow error: address + \
                                length exceeds 0x3F')
        else:
            raise ValueError('read_memory: address out of range')
