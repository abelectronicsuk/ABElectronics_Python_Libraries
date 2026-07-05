#!/usr/bin/env python

"""
================================================
IOPi Python Library
================================================

Library for the IO Pi Plus and IO Pi Zero expansion boards from AB Electronics UK
for the Raspberry Pi and other compatible single-board computers.

https://www.abelectronics.co.uk/p/54/io-pi-plus

Designed for use with the Microchip MCP23017 I/O controller.

This library provides functions for reading digital inputs and outputs on the MCP23017 I/O controller.

Each MCP23017 chip is split into two 8-bit ports.  Port 0 controls
pins 1 to 8, while Port 1 controls pins 9 to 16.

When writing to or reading from a bus or port, the least significant bit
represents the lowest numbered pin on the selected port.

================================================
MIT Licence

Copyright (c) 2025 AB Electronics UK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
================================================

Requires smbus2 or python smbus to be installed
"""
from typing import Optional, Union
from enum import IntEnum

try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python3-smbus or smbus2 not found")
import re
import platform


class IOPi(object):
    """
    The MCP23017 chip is split into two 8-bit ports.  Port 0 controls pins
    1 to 8, while Port 1 controls pins 9 to 16.
    When writing to or reading from a bus or port, the least significant bit
    represents the lowest numbered pin on the selected port.
    #
    """

    # Define registers values from the datasheet
    IODIRA = 0x00  # IO direction A - 1= input 0 = output
    IODIRB = 0x01  # IO direction B - 1= input 0 = output
    # Input polarity A - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLA = 0x02
    # Input polarity B - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLB = 0x03
    # The GPINTEN register controls the interrupt-on-change feature for each
    # pin on port A.
    GPINTENA = 0x04
    # The GPINTEN register controls the interrupt-on-change feature for each
    # pin on port B.
    GPINTENB = 0x05
    # Default value for port A - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite to the register bit, an interrupt occurs.
    DEFVALA = 0x06
    # Default value for port B - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite to the register bit, an interrupt occurs.
    DEFVALB = 0x07
    # Interrupt control register for port A. If 1 interrupt triggers when the
    # pin matches the default value, if 0 the interrupt triggers on state
    # change
    INTCONA = 0x08
    # Interrupt control register for port B. If 1 interrupt triggers when the
    # pin matches the default value, if 0 the interrupt triggers on state
    # change
    INTCONB = 0x09
    IOCON = 0x0A  # see datasheet for configuration register
    GPPUA = 0x0C  # pull-up resistors for port A
    GPPUB = 0x0D  # pull-up resistors for port B
    # The INTF register reflects the interrupt condition on the port A pins of
    # any pin that is enabled for interrupts. A set bit indicates that the
    # associated pin caused the interrupt event.
    INTFA = 0x0E
    # The INTF register reflects the interrupt condition on the port B pins of
    # any pin that is enabled for interrupts.  A set bit indicates that the
    # associated pin caused the interrupt event.
    INTFB = 0x0F
    # The INTCAP register captures the GPIO port A value at the time the
    # interrupt occurred.
    INTCAPA = 0x10
    # The INTCAP register captures the GPIO port B value at the time the
    # interrupt occurred.
    INTCAPB = 0x11
    GPIOA = 0x12  # data port A
    GPIOB = 0x13  # data port B
    OLATA = 0x14  # output latches A
    OLATB = 0x15  # output latches B

    # variables
    __io_address = 0x20  # I2C address
    # initial configuration
    # see the IOCON page in the MCP23017 datasheet for more information.
    __conf = 0x02
    __bus = None

    def __init__(self, address: int, initialise=True, bus=None) -> None:
        """
        IOPi object initialisation

        :param address: I2C address for the target device, 0x20 to 0x27
        :type address: int
        :param initialise: True = direction set as inputs, pull-ups disabled,
                           ports are not inverted.
                           False = device state unaltered., defaults to True
        :type initialise: bool, optional
        :param bus: I2C bus number.  If no value is set, the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int, optional
        """

        if address < 0x20 or address > 0x27:
            raise ValueError("__init__ i2c address out of range: 0x20 to 0x27")
        if type(initialise) is not bool:
            raise ValueError("__init__ initialise must be bool: True of False")

        self.__io_address = address
        self.__bus = self.__get_smbus(bus)

        try:
            self.__bus.write_byte_data(self.__io_address, self.IOCON, self.__conf)

            if initialise is True:
                self.__bus.write_word_data(self.__io_address, self.IODIRA, 0xFFFF)
                self.__bus.write_word_data(self.__io_address, self.GPPUA, 0x0000)
                self.__bus.write_word_data(self.__io_address, self.IPOLA, 0x0000)

        except IOError as err:
            raise IOError(f"I/O error: {err}")

        return

    # local methods
    @staticmethod
    def __detect_raspberry_pi_bus():
        """
        Internal method to detect the appropriate I2C bus for Raspberry Pi models

        :return: I2C bus number
        :rtype: int
        """
        for line in open('/proc/cpuinfo').readlines():
            model = re.match('(.*?)\\s*:\\s*(.*)', line)
            if model:
                name, value = model.group(1), model.group(2)
                if name == "Revision":
                    if value[-4:] in ('0002', '0003'):
                        return 0  # original model A or B
                    else:
                        return 1  # later models

        return 1  # default to bus 1 if revision can't be determined

    @staticmethod
    def __get_smbus(bus):
        """
        Internal method for getting an instance of the i2c bus

        :param bus: I2C bus number.  If the value is None, the class will
                    try to find the i2c bus automatically using the device name
        :type bus: int
        :return: i2c bus for the target device
        :rtype: SMBus
        :raises IOError: Could not open the i2c bus
        """

        # Use the provided bus number if available
        if bus is not None:
            i2c_bus = bus
        else:
            # Map device names to their corresponding bus numbers
            device_bus_map = {
                "orangepione": 0,  # Orange Pi One
                "orangepizero2": 3,  # Orange Pi Zero 2
                "orangepiplus": 0,  # Orange Pi Plus
                "orangepipcplus": 0,  # Orange Pi PC Plus
                "linaro-alip": 1,  # Asus Tinker Board
                "bpi-m2z": 0,  # Banana Pi BPI M2 Zero Ubuntu
                "bpi-iot-ros-ai": 0,  # Banana Pi BPI M2 Zero Raspbian
                "radxa-dragon-q6a": 6,  # Radxa Dragon Q6A Radxa OS
            }

            # Get device name
            device = platform.uname()[1]

            # Get the bus number from the map or detect for Raspberry Pi
            if device in device_bus_map:
                i2c_bus = device_bus_map[device]
            elif device == "raspberrypi":
                i2c_bus = IOPi.__detect_raspberry_pi_bus()
            else:
                i2c_bus = 1  # Default to bus 1 for unknown devices

        try:
            return SMBus(i2c_bus)
        except FileNotFoundError:
            raise FileNotFoundError("Bus not found. Check that you have selected the correct I2C bus.")
        except IOError as err:
            raise IOError(f"I/O error: {err}")

    @staticmethod
    def __check_bit(byte, bit):
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
        return byte

    def __set_pin(self, pin: int, value: int, a_register: int, b_register: int) -> None:

        """
            Internal method for setting the value of a single bit
            within the device registers

            :param pin: 1 to 16
            :type pin: int
            :param value: 0 or 1
            :type value: int
            :param a_register: A register, e.g. IODIRA
            :type a_register: int
            :param b_register: B register, e.g. IODIRB
            :type b_register: int
            :raises ValueError: pin out of range: 1 to 16
            :raises ValueError: value out of range: 0 or 1
            """

        if 1 <= pin <= 8:
            reg = a_register
            pin = pin - 1
        elif 9 <= pin <= 16:
            reg = b_register
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")
        try:
            current_value = self.__bus.read_byte_data(self.__io_address, reg)
            new_value = self.__update_byte(current_value, pin, value)
            self.__bus.write_byte_data(self.__io_address, reg, new_value)

        except IOError as err:
            raise IOError(f"I/O error: {err}")

        return

    def __get_pin(self, pin: int, a_register: int, b_register: int) -> int:

        """
            Internal method for getting the value of a single bit
            within the device registers

            :param pin: 1 to 16
            :type pin: int
            :param a_register: A register, e.g. IODIRA
            :type a_register: int
            :param b_register: B register, e.g. IODIRB
            :type b_register: int
            :raises ValueError: pin out of range: 1 to 16
            :return: 0 or 1
            :rtype: int
            """
        try:
            if 1 <= pin <= 8:
                current_value = self.__bus.read_byte_data(self.__io_address, a_register)
                value = self.__check_bit(current_value, pin - 1)
            elif 9 <= pin <= 16:
                current_value = self.__bus.read_byte_data(self.__io_address, b_register)
                value = self.__check_bit(current_value, pin - 9)
            else:
                raise ValueError("pin out of range: 1 to 16")
        except IOError as err:
            raise IOError(f"I/O error: {err}")

        return value

    def __set_port(self, port: int, value: int, a_register: int, b_register: int) -> None:

        """
            Internal method for setting the value of a device register

            :param port: 0 or 1
            :type port: int
            :param value: 0 to 255 (0xFF)
            :type value: int
            :param a_register: A register, e.g. IODIRA
            :type a_register: int
            :param b_register: B register, e.g. IODIRB
            :type b_register: int
            :raises ValueError: port out of range: 0 or 1
            :raises ValueError: value out of range: 0 to 255 (0xFF)
            """
        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        try:
            if port == 0:
                self.__bus.write_byte_data(self.__io_address, a_register, value)
            else:
                self.__bus.write_byte_data(self.__io_address, b_register, value)
        except IOError as err:
            raise IOError(f"I/O error: {err}")

        return

    def __get_port(self, port: int, a_register: int, b_register: int) -> int:

        """
            Internal method for getting the value of a device register

            :param port: 0 or 1
            :type port: int
            :param a_register: A register, e.g. IODIRA
            :type a_register: int
            :param b_register: B register, e.g. IODIRB
            :type b_register: int
            :raises ValueError: port out of range: 0 or 1
            :return: 0 to 255 (0xFF)
            :rtype: int
            """
        try:
            if port == 0:
                return self.__bus.read_byte_data(self.__io_address, a_register)
            elif port == 1:
                return self.__bus.read_byte_data(self.__io_address, b_register)
            else:
                raise ValueError("port out of range: 0 or 1")
        except IOError as err:
            raise IOError(f"I/O error: {err}")

    def __set_bus(self, value: int, a_register: int) -> None:

        """
            Internal method for writing a 16-bit value to
            two consecutive device registers

            :param value: 0 to 65535 (0xFFFF)
            :type value: int
            :param a_register: A register, e.g. IODIRA
            :type a_register: int
            :raises ValueError: value out of range: 0 to 65535 (0xFFFF)
            """
        try:
            if 0x0000 <= value <= 0xFFFF:
                self.__bus.write_word_data(self.__io_address, a_register, value)
            else:
                raise ValueError('value out of range: 0 to 65535 (0xFFFF)')
        except IOError as err:
            raise IOError(f"I/O error: {err}")
        return

    # public methods

    def set_pin_direction(self, pin: int, value: int) -> None:
        """
        Set the IO direction for an individual pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = input, 0 = output
        :type value: int
        :raises ValueError:  pin is out of range, 1 to 16
        :raises ValueError:  value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.IODIRA, self.IODIRB)
        return

    def get_pin_direction(self, pin: int) -> int:
        """
        Get the IO direction for an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError:  pin is out of range, 1 to 16
        :return: 1 = input, 0 = output
        :rtype: int
        """
        return self.__get_pin(pin, self.IODIRA, self.IODIRB)

    def set_port_direction(self, port: int, value: int) -> None:
        """
        Set the direction for an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError:  port is out of range, 0 or 1
        :raises ValueError:  value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.IODIRA, self.IODIRB)
        return

    def get_port_direction(self, port: int) -> int:
        """
        Get the direction from an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError:  port is out of range, 0 or 1
        """
        return self.__get_port(port, self.IODIRA, self.IODIRB)

    def set_bus_direction(self, value: int) -> None:
        """
        Set the direction for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError:  value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.IODIRA)
        return

    def get_bus_direction(self) -> int:
        """
        Get the direction for an IO bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = input, 0 = output
        :rtype: int
        """
        try:
            return self.__bus.read_word_data(self.__io_address, self.IODIRA)
        except IOError as err:
            raise IOError(f"I/O error: {err}")

    def set_pin_pullup(self, pin: int, value: int) -> None:
        """
        Set the internal 100K pull-up resistors for an individual pin

        :param pin: pin to update; 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError:  pin is out of range, 1 to 16
        :raises ValueError:  value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.GPPUA, self.GPPUB)
        return

    def get_pin_pullup(self, pin: int) -> int:
        """
        Get the internal 100K pull-up resistors for an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError:  pin is out of range, 1 to 16
        :return: 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__get_pin(pin, self.GPPUA, self.GPPUB)

    def set_port_pullups(self, port: int, value: int) -> None:
        """
        Set the internal 100K pull-up resistors for the selected IO port

         :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError:  port is out of range, 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.GPPUA, self.GPPUB)
        return

    def get_port_pullups(self, port: int) -> int:
        """
        Get the internal pull-up status for the selected IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError:  port is out of range, 0 or 1
        """
        return self.__get_port(port, self.GPPUA, self.GPPUB)

    def set_bus_pullups(self, value: int) -> None:
        """
        Set internal 100K pull-up resistors for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled; 0 = disabled
        :type value: int
        :raises ValueError:  value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPPUA)
        return

    def get_bus_pullups(self) -> int:
        """
        Get the internal 100K pull-up resistors for an IO bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__bus.read_word_data(self.__io_address, self.GPPUA)

    def write_pin(self, pin: int, value: int) -> None:
        """
        Write to an individual pin 1-16

        :param pin: pin to update 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError:  pin is out of range, 1 to 16
        :raises ValueError:  value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.GPIOA, self.GPIOB)
        return

    def write_port(self, port: int, value: int) -> None:
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
        self.__set_port(port, value, self.GPIOA, self.GPIOB)
        return

    def write_bus(self, value: int) -> None:
        """
        Write to all pins on the selected bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = logic high, 0 = logic low
        :type value: int
        :raises ValueError:  value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPIOA)
        return

    def read_pin(self, pin: int) -> int:
        """
        Read the value of an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: [type]
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: [description]
        :return: 0 = logic level low, 1 = logic level high
        :rtype: [type]
        """
        return self.__get_pin(pin, self.GPIOA, self.GPIOB)

    def read_port(self, port: int) -> int:
        """
        Read all pins on the selected port

        :param port: 0 = pins 1 to 8, port 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        """
        return self.__get_port(port, self.GPIOA, self.GPIOB)

    def read_bus(self) -> int:
        """
        Read all pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF)
        :rtype: int
        """
        return self.__bus.read_word_data(self.__io_address, self.GPIOA)

    def invert_pin(self, pin: int, value: int) -> None:
        """
        Invert the polarity of the selected pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: value out of range: 0 or 1
        """
        self.__set_pin(pin, value, self.IPOLA, self.IPOLB)
        return

    def get_pin_polarity(self, pin: int) -> int:
        """
        Get the polarity of the selected pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError:  pin is out of range, 1 to 16
        :return: 0 = the same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__get_pin(pin, self.IPOLA, self.IPOLB)

    def invert_port(self, port: int, value: int) -> None:
        """
        Invert the polarity of the pins on a selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF).  For each bit
                      0 = the same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError:  port is out of range, 0 or 1
        :raises ValueError:  value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.IPOLA, self.IPOLB)
        return

    def get_port_polarity(self, port: int) -> int:
        """
        Get the polarity for the selected IO port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError:  port is out of range, 0 or 1
        """
        return self.__get_port(port, self.IPOLA, self.IPOLB)

    def invert_bus(self, value: int) -> None:
        """
        Invert the polarity of the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError:  value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.IPOLA)
        return

    def get_bus_polarity(self) -> int:
        """
        Get the polarity of the pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF). For each bit
                 0 = same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__bus.read_word_data(self.__io_address, self.IPOLA)

    def mirror_interrupts(self, value: int) -> None:
        """
        Sets whether the interrupt pins INT A and INT B are independently
        connected to each port or internally connected

        :param value: 1 = The INT pins are internally connected,
                      0 = The INT pins are not connected.
                      INT A is associated with PortA and
                      INT B is associated with PortB
        :type value: int
        :raises ValueError: value out of range: 0 or 1
        """

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        conf = self.__bus.read_byte_data(self.__io_address, self.IOCON)

        if value == 0:
            conf = self.__update_byte(conf, 6, 0)
            self.__bus.write_byte_data(self.__io_address, self.IOCON, conf)
        if value == 1:
            conf = self.__update_byte(self.__conf, 6, 1)
            self.__bus.write_byte_data(self.__io_address, self.IOCON, conf)
        return

    def set_interrupt_polarity(self, value: int) -> None:
        """
        This sets the polarity of the INT output pins

        :param value: 1 = Active-high.  0 = Active-low.
        :type value: int
        :raises ValueError: value out of range: 0 or 1
        """

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        conf = self.__bus.read_byte_data(self.__io_address, self.IOCON)

        if value == 0:
            conf = self.__update_byte(conf, 1, 0)
            self.__bus.write_byte_data(self.__io_address, self.IOCON, conf)
        if value == 1:
            conf = self.__update_byte(self.__conf, 1, 1)
            self.__bus.write_byte_data(self.__io_address, self.IOCON, conf)

        return

    def get_interrupt_polarity(self) -> int:
        """
        Get the polarity of the INT output pins
        :return: 1 = Active-high.  0 = Active-low.
        :rtype: int
        """
        return self.__check_bit(self.__bus.read_byte_data(self.__io_address,
                                                          self.IOCON), 1)

    def set_interrupt_type(self, port: int, value: int) -> None:
        """
        Sets the type of interrupt for each pin on the selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = interrupt triggers when the pin matches
                      the default value, 0 = interrupt fires on state change
        :type value: int
        :raises ValueError:  port is out of range, 0 or 1
        :raises ValueError:  value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.INTCONA, self.INTCONB)
        return

    def get_interrupt_type(self, port: int) -> int:
        """
        Get the type of interrupt for each pin on the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: 8-bit number 0 to 255 (0xFF)
                 For each bit 1 = interrupt triggers when the pin matches
                 the default value, 0 = interrupt fires on state change
        :rtype: int
        :raises ValueError: port is out of range, 0 or 1
        """
        return self.__get_port(port, self.INTCONA, self.INTCONB)

    def set_interrupt_defaults(self, port: int, value: int) -> None:
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite of the register bit, an
        interrupt occurs.

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
        :type value: int
        :raises ValueError: port is out of range, 0 or 1
        :raises ValueError: value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.DEFVALA, self.DEFVALB)
        return

    def get_interrupt_defaults(self, port: int) -> int:
        """
        Get the interrupt default value for each pin on the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: 8-bit number 0 to 255 (0xFF)
        :rtype: int
        :raises ValueError: port is out of range, 0 or 1
        """
        return self.__get_port(port, self.DEFVALA, self.DEFVALB)

    def set_interrupt_on_pin(self, pin: int, value: int) -> None:
        """
        Enable interrupts for the selected pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: pin is out of range, 1 to 16
        :raises ValueError: value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.GPINTENA, self.GPINTENB)
        return

    def get_interrupt_on_pin(self, pin: int) -> int:
        """
        Gets whether the interrupt is enabled for the selected pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: pin is out of range, 1 to 16
        :return: 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__get_pin(pin, self.GPINTENA, self.GPINTENB)

    def set_interrupt_on_port(self, port: int, value: int) -> None:
        """
        Enable interrupts for the pins on the selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: port is out of range, 0 or 1
        :raises ValueError: value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.GPINTENA, self.GPINTENB)
        return

    def get_interrupt_on_port(self, port: int) -> int:
        """
        Gets whether the interrupts are enabled for the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        :raises ValueError: port is out of range, 0 or 1
        """
        return self.__get_port(port, self.GPINTENA, self.GPINTENB)

    def set_interrupt_on_bus(self, value: int) -> None:
        """
        Enable interrupts for the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPINTENA)
        return

    def get_interrupt_on_bus(self) -> int:
        """
        Gets whether the interrupts are enabled for the bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__bus.read_word_data(self.__io_address, self.GPINTENA)

    def read_interrupt_status(self, port: int) -> int:
        """
        Read the interrupt status for the pins on the selected port
        interrupt trigger

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: interrupt status for the selected port
        :rtype: int
        """
        return self.__get_port(port, self.INTFA, self.INTFB)

    def read_interrupt_capture(self, port: int) -> int:
        """
        Read the value from the selected port at the time of the last
        interrupt trigger

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: port value at the time of the last interrupt trigger
        :rtype: int
        """
        return self.__get_port(port, self.INTCAPA, self.INTCAPB)

    def reset_interrupts(self) -> None:
        """
        Reset interrupts A and B to 0
        """
        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return

    class Port:
        """Represents a single 8-bit port on the IO Pi board.

        This class encapsulates all port-related operations and provides
        an interface for working with individual ports.

        Attributes:
            _parent (IOPi): Reference to the parent IOPi instance
            _port_num (int): Port number (0 for port A, 1 for port B)
        """

        def __init__(self, parent: 'IOPi', port_num: int) -> None:
            """Initialise a Port instance.

            Args:
                parent: Reference to the parent IOPi instance
                port_num: Port number (0 for port A, 1 for port B)

            Raises:
                ValueError: If port_num is not 0 or 1
            """
            if not isinstance(port_num, int):
                raise TypeError("Port number must be an integer")
            if port_num not in (0, 1):
                raise ValueError("Port number must be 0 (Port A) or 1 (Port B)")

            self._parent = parent
            self._port_num = port_num

        @property
        def value(self) -> int:
            """Current value of the port (0-255)."""
            return self._parent.read_port(self._port_num)

        @value.setter
        def value(self, value: int) -> None:
            """Set the value of the port.

            Args:
                value: 8-bit value to write (0-255)
            """
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Value must be between 0 and 255")
            self._parent.write_port(self._port_num, value)

        @property
        def direction(self) -> int:
            """Port direction configuration (1 = input, 0 = output)."""
            return self._parent.get_port_direction(self._port_num)

        @direction.setter
        def direction(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Direction must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Direction must be between 0 and 255")
            self._parent.set_port_direction(self._port_num, value)

        @property
        def pullups(self) -> int:
            """Pullup resistor configuration (1 = enabled, 0 = disabled)."""
            return self._parent.get_port_pullups(self._port_num)

        @pullups.setter
        def pullups(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Value must be between 0 and 255")
            self._parent.set_port_pullups(self._port_num, value)

        @property
        def polarity(self) -> int:
            """Polarity inversion configuration (1 = inverted, 0 = normal)."""
            return self._parent.get_port_polarity(self._port_num)

        @polarity.setter
        def polarity(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Value must be between 0 and 255")
            self._parent.invert_port(self._port_num, value)

        @property
        def interrupts(self) -> int:
            """Interrupt enabled status (1 = enabled, 0 = disabled)."""
            return self._parent.get_interrupt_on_port(self._port_num)

        @interrupts.setter
        def interrupts(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Value must be between 0 and 255")
            self._parent.set_interrupt_on_port(self._port_num, value)

        @property
        def interrupt_defaults(self) -> int:
            """Interrupt default values."""
            return self._parent.get_interrupt_defaults(self._port_num)

        @interrupt_defaults.setter
        def interrupt_defaults(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 255:
                raise ValueError("Value must be between 0 and 255")
            self._parent.set_interrupt_defaults(self._port_num, value)

        @property
        def interrupt_status(self) -> int:
            """Current interrupt status."""
            return self._parent.read_interrupt_status(self._port_num)

        @property
        def interrupt_capture(self) -> int:
            """Interrupt capture values."""
            return self._parent.read_interrupt_capture(self._port_num)

        def __str__(self) -> str:
            """Return string representation of the port."""
            return f"Port {'A' if self._port_num == 0 else 'B'}: {bin(self.value)[2:].zfill(8)}"

        def __repr__(self) -> str:
            """Return detailed string representation of the port."""
            return (f"Port(num={self._port_num}, value={self.value}, "
                   f"direction={self.direction})")

        def __int__(self) -> int:
            """Allow direct conversion of port to integer value."""
            return self.value

        def __index__(self) -> int:
            """Allow port to be used in binary operations."""
            return self.value


    class Pin:
        """Represents a single pin on the IO Pi board.

        This class encapsulates all pin-related operations and provides
        an interface for working with individual pins.
        """

        def __init__(self, parent: 'IOPi', pin_num: int):
            """Initialise a Pin instance.

            Args:
                parent: Reference to the parent IOPi instance
                pin_num: Pin number (0-15)

            Raises:
                ValueError: If pin_num is not 0-15
            """
            if not isinstance(pin_num, int):
                raise TypeError("Pin number must be an integer")
            if not 0 <= pin_num <= 15:
                raise ValueError("Pin number must be between 0 and 15")

            self._parent = parent
            self._pin_num = pin_num
            self._port_num = pin_num // 8
            self._pin_index = pin_num % 8

        @property
        def value(self) -> int:
            """Current value of the pin (0 or 1)."""
            return self._parent.read_pin(self._pin_num)

        @value.setter
        def value(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if value not in (0, 1):
                raise ValueError("Value must be 0 or 1")
            self._parent.write_pin(self._pin_num, value)

        @property
        def direction(self) -> int:
            """Pin direction (1 = input, 0 = output)."""
            return (self._parent.get_port_direction(self._port_num) >> self._pin_index) & 1

        @direction.setter
        def direction(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Direction must be an integer")
            if value not in (0, 1):
                raise ValueError("Direction must be 0 or 1")
            current = self._parent.get_port_direction(self._port_num)
            if value:
                new_value = current | (1 << self._pin_index)
            else:
                new_value = current & ~(1 << self._pin_index)
            self._parent.set_port_direction(self._port_num, new_value)

        @property
        def pullup(self) -> int:
            """Pullup resistor state (1 = enabled, 0 = disabled)."""
            return (self._parent.get_port_pullups(self._port_num) >> self._pin_index) & 1

        @pullup.setter
        def pullup(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if value not in (0, 1):
                raise ValueError("Value must be 0 or 1")
            current = self._parent.get_port_pullups(self._port_num)
            if value:
                new_value = current | (1 << self._pin_index)
            else:
                new_value = current & ~(1 << self._pin_index)
            self._parent.set_port_pullups(self._port_num, new_value)

        @property
        def polarity(self) -> int:
            """Polarity inversion state (1 = inverted, 0 = normal)."""
            return (self._parent.get_port_polarity(self._port_num) >> self._pin_index) & 1

        @polarity.setter
        def polarity(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if value not in (0, 1):
                raise ValueError("Value must be 0 or 1")
            current = self._parent.get_port_polarity(self._port_num)
            if value:
                new_value = current | (1 << self._pin_index)
            else:
                new_value = current & ~(1 << self._pin_index)
            self._parent.invert_port(self._port_num, new_value)

        def __int__(self) -> int:
            """Allow direct conversion of pin to integer value."""
            return self.value

        def __bool__(self) -> bool:
            """Allow direct use of pin in boolean contexts."""
            return bool(self.value)

        def __str__(self) -> str:
            """Return string representation of the pin."""
            return f"Pin {self._pin_num}: {self.value}"

        def __repr__(self) -> str:
            """Return detailed string representation of the pin."""
            return (f"Pin(num={self._pin_num}, value={self.value}, "
                    f"direction={'input' if self.direction else 'output'})")

    class Bus:
        """Represents a collection of pins that can be treated as a single entity.

        This class allows working with multiple pins as if they were a single bus,
        supporting operations across ports.
        """

        def __init__(self, parent: 'IOPi'):
            """Initialise a Bus instance.

            Args:
                parent: Reference to the parent IOPi instance
            """
            self._parent = parent

        @property
        def value(self) -> int:
            """Current value of the bus as an integer."""
            result = self._parent.read_bus()
            return result

        @value.setter
        def value(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Value must be an integer")
            if not 0 <= value <= 0xFFFF:
                raise ValueError(f"Value must be between 0 and 0xFFFF")

            self._parent.write_bus(value)

        @property
        def direction(self) -> int:
            """Direction configuration for all pins in the bus."""
            result = self._parent.get_bus_direction()
            return result

        @direction.setter
        def direction(self, value: int) -> None:
            if not isinstance(value, int):
                raise TypeError("Direction must be an integer")
            if not 0 <= value <= 0xFFFF:
                raise ValueError(f"Direction must be between 0 and 0xFFFF")

            self._parent.set_bus_direction(value)

        def __int__(self) -> int:
            """Allow direct conversion of bus to integer value."""
            return self.value

        def __repr__(self) -> str:
            """Return detailed string representation of the bus."""
            return f"Bus(direction={self.direction}, value={self.value})"

        def __len__(self) -> int:
            """Return the number of pins in the bus."""
            return 16

