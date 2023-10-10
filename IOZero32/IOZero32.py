#!/usr/bin/env python
"""
================================================
AB Electronics UK: IO Zero 32

Requires smbus2 or python smbus to be installed
================================================

32-Channel Port Expander based on the PCA9535.
The PCA9535 chip is split into two 8-bit ports.  Port 0 controls
pins 1 to 8 while Port 1 controls pins 9 to 16.
When writing to or reading from a bus or port the least significant bit
represents the lowest numbered pin on the selected port.
"""
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
import re
import platform


class IOZero32(object):
    """
    The PCA9535 contains a 16-bit bus split into two 8-bit ports.  
    Port 0 controls pins 1 to 8 while Port 1 controls pins 9 to 16.
    #
    """

    # Define registers values from the datasheet
    
    INPUTPORT0  = 0x00  # Command byte Input port 0
    INPUTPORT1  = 0x01  # Command byte Input port 1
    OUTPUTPORT0 = 0x02  # Command byte Output port 0
    OUTPUTPORT1 = 0x03  # Command byte Output port 1
    INVERTPORT0 = 0x04  # Command byte Polarity Inversion port 0
    INVERTPORT1 = 0x05  # Command byte Polarity Inversion port 1
    CONFIGPORT0 = 0x06  # Command byte Configuration port 0
    CONFIGPORT1 = 0x07  # Command byte Configuration port 1

    # variables
    __ioaddress = 0x20  # I2C address
    __bus = None

    def __init__(self, address, bus=None):
        """
        IOZero32 object initialisation

        :param address: i2c address for the target device, 0x20 to 0x27
        :type address: int       
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int, optional
        """

        if address < 0x20 or address > 0x27:
            raise ValueError("__init__ i2c address out of range: 0x20 to 0x27")

        self.__ioaddress = address
        self.__bus = self.__get_smbus(bus)

        return

    # local methods
    @staticmethod
    def __get_smbus(bus):
        """
        Internal method for getting an instance of the i2c bus

        :param bus: I2C bus number.  If the value is None the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int
        :return: I2C bus for the target device
        :rtype: SMBus
        :raises IOError: Could not open the i2c bus
        """
        i2c__bus = 1
        if bus is not None:
            i2c__bus = bus
        else:
            # detect the device that is being used
            device = platform.uname()[1]

            if device == "orangepione":  # orange pi one
                i2c__bus = 0

            elif device == "orangepizero2": # orange pi zero 2
                i2c__bus = 3

            elif device == "orangepiplus":  # orange pi plus
                i2c__bus = 0

            elif device == "orangepipcplus":  # orange pi pc plus
                i2c__bus = 0

            elif device == "linaro-alip":  # Asus Tinker Board
                i2c__bus = 1

            elif device == "bpi-m2z":  # Banana Pi BPI M2 Zero Ubuntu
                i2c__bus = 0

            elif device == "bpi-iot-ros-ai":  # Banana Pi BPI M2 Zero Raspbian
                i2c__bus = 0

            elif device == "raspberrypi":  # running on raspberry pi
                # detect i2C port number and assign to i2c__bus
                for line in open('/proc/cpuinfo').readlines():
                    model = re.match('(.*?)\\s*:\\s*(.*)', line)
                    if model:
                        (name, value) = (model.group(1), model.group(2))
                        if name == "Revision":
                            if value[-4:] in ('0002', '0003'):
                                i2c__bus = 0  # original model A or B
                            else:
                                i2c__bus = 1  # later models
                            break
        try:
            return SMBus(i2c__bus)
        except IOError:
            raise 'Could not open the i2c bus'

    @staticmethod
    def __checkbit(byte, bit):
        """
        Internal method for reading the value of a single bit within a byte

        :param byte: input value
        :type byte: int
        :param bit: location within value to check
        :type bit: int
        :return: value of the selected bit, 0 or 1
        :rtype: int
        """
        value = 0
        if byte & (1 << bit):
            value = 1
        return value

    @staticmethod
    def __updatebyte(byte, bit, value):
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

    def __set_pin(self, pin, value, a_register, b_register):
        """
        Internal method for setting the value of a single bit
        within the device registers

        :param pin: 1 to 16
        :type pin: int
        :param value: 0 or 1
        :type value: int
        :param a_register: register for port 0
        :type a_register: int
        :param b_register: register for port 1
        :type b_register: int
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: value out of range: 0 or 1
        """
        reg = None
        if pin >= 1 and pin <= 8:
            reg = a_register
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = b_register
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

        return

    def __get_pin(self, pin, a_register, b_register):
        """
        Internal method for getting the value of a single bit
        within the device registers

        :param pin: 1 to 16
        :type pin: int
        :param a_register: register for port 0
        :type a_register: int
        :param b_register: register for port 1
        :type b_register: int
        :raises ValueError: pin out of range: 1 to 16
        :return: 0 or 1
        :rtype: int
        """
        value = 0

        if pin >= 1 and pin <= 8:
            curval = self.__bus.read_byte_data(self.__ioaddress, a_register)
            value = self.__checkbit(curval, pin - 1)
        elif pin >= 9 and pin <= 16:
            curval = self.__bus.read_byte_data(self.__ioaddress, b_register)
            value = self.__checkbit(curval, pin - 9)
        else:
            raise ValueError("pin out of range: 1 to 16")

        return value

    def __set_port(self, port, value, a_register, b_register):
        """
        Internal method for setting the value of a device register

        :param port: 0 or 1
        :type port: int
        :param value: 0 to 255 (0xFF)
        :type value: int
        :param a_register: register for port 0
        :type a_register: int
        :param b_register: register for port 1
        :type b_register: int
        :raises ValueError: port out of range: 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """
        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, a_register, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, b_register, value)
        return

    def __get_port(self, port, a_register, b_register):
        """
        Internal method for getting the value of a device register

        :param port: 0 or 1
        :type port: int
        :param a_register: register for port 0
        :type a_register: int
        :param b_register: register for port 1
        :type b_register: int
        :raises ValueError: port out of range: 0 or 1
        :return: 0 to 255 (0xFF)
        :rtype: int
        """
        if port == 0:
            return self.__bus.read_byte_data(self.__ioaddress, a_register)
        elif port == 1:
            return self.__bus.read_byte_data(self.__ioaddress, b_register)
        else:
            raise ValueError("port out of range: 0 or 1")
        return

    def __set_bus(self, value, a_register):
        """
        Internal method for writing a 16-bit value to
        two consecutive device registers

        :param value: 0 to 65535 (0xFFFF)
        :type value: int
        :param a_register: register for port 0
        :type a_register: int
        :raises ValueError: value out of range: 0 to 65535 (0xFFFF)
        """
        if value >= 0x0000 and value <= 0xFFFF:
            self.__bus.write_word_data(self.__ioaddress, a_register, value)
        else:
            raise ValueError('value out of range: 0 to 65535 (0xFFFF)')
        return

    # public methods

    def set_pin_direction(self, pin, value):
        """
        Set the IO direction for an individual pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = input, 0 = output
        :type value: int
        :raises ValueError: pin is out of range, 1 to 16
        :raises ValueError: value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.CONFIGPORT0 , self.CONFIGPORT1)
        return

    def get_pin_direction(self, pin):
        """
        Get the IO direction for an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: pin is out of range, 1 to 16
        :return: 1 = input, 0 = output
        :rtype: int
        """
        return self.__get_pin(pin, self.CONFIGPORT0 , self.CONFIGPORT1)

    def set_port_direction(self, port, value):
        """
        Set the direction for an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError: port is out of range, 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.CONFIGPORT0 , self.CONFIGPORT1)
        return

    def get_port_direction(self, port):
        """
        Get the direction from an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: port is out of range, 0 or 1
        """
        return self.__get_port(port, self.CONFIGPORT0 , self.CONFIGPORT1)

    def set_bus_direction(self, value):
        """
        Set the direction for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError: value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.CONFIGPORT0)
        return

    def get_bus_direction(self):
        """
        Get the direction for an IO bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = input, 0 = output
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.CONFIGPORT0)

    def write_pin(self, pin, value):
        """
        Write to an individual pin 1 - 16

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: pin is out of range, 1 to 16
        :raises ValueError: value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.OUTPUTPORT0, self.OUTPUTPORT1)
        return

    def write_port(self, port, value):
        """
        Write to all pins on the selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = logic high, 0 = logic low
        :type value: int
        :raises ValueError: port out of range: 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.OUTPUTPORT0, self.OUTPUTPORT1)
        return

    def write_bus(self, value):
        """
        Write to all pins on the selected bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = logic high, 0 = logic low
        :type value: int
        :raises ValueError: value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.OUTPUTPORT0)
        return

    def read_pin(self, pin):
        """
        Read the value of an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: [type]
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: [description]
        :return: 0 = logic level low, 1 = logic level high
        :rtype: [type]
        """
        return self.__get_pin(pin, self.INPUTPORT0, self.INPUTPORT1)

    def read_port(self, port):
        """
        Read all pins on the selected port

        :param port: 0 = pins 1 to 8, port 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        """
        return self.__get_port(port, self.INPUTPORT0, self.INPUTPORT1)

    def read_bus(self):
        """
        Read all pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF)
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.INPUTPORT0)

    def set_pin_polarity(self, pin, value):
        """
        Set the polarity of the selected pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: value out of range: 0 or 1
        """
        self.__set_pin(pin, value, self.INVERTPORT0, self.INVERTPORT1)
        return

    def get_pin_polarity(self, pin):
        """
        Get the polarity of the selected pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: pin is out of range, 1 to 16
        :return: 0 = same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__get_pin(pin, self.INVERTPORT0, self.INVERTPORT1)

    def set_port_polarity(self, port, value):
        """
        Set the polarity of the pins on a selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: port is out of range, 0 or 1
        :raises ValueError: value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.INVERTPORT0, self.INVERTPORT1)
        return

    def get_port_polarity(self, port):
        """
        Get the polarity for the selected IO port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: port is out of range, 0 or 1
        """
        return self.__get_port(port, self.INVERTPORT0, self.INVERTPORT1)

    def set_bus_polarity(self, value):
        """
        Set the polarity of the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.INVERTPORT0)
        return

    def get_bus_polarity(self):
        """
        Get the polarity of the pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF). For each bit
                 0 = same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.INVERTPORT0)