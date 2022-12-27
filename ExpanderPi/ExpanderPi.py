#!/usr/bin/env python
"""
================================================
AB Electronics UK Expander Pi

Requires smbus2 or python smbus to be installed

================================================
"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
try:
    import spidev
except ImportError:
    raise ImportError(
        "spidev not found.")
import re
import platform
import datetime


"""
Private Classes
"""


class _ABEHelpers:
    """
    Local Functions used across all Expander Pi classes
    """

    @staticmethod
    def updatebyte(byte, bit, value):
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
    def get_smbus(bus):
        """
        Internal method for getting an instance of the I2C bus

        :param bus: I2C bus number.  If the value is None the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int
        :return: I2C bus for target device
        :rtype: SMBus
        :raises IOError: Could not open the I2C bus
        """
        i2c__bus = 1
        if bus is not None:
            i2c__bus = bus
        else:
            # detect the device that is being used
            device = platform.uname()[1]

            if device == "orangepione":  # orange pi one
                i2c__bus = 0

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
            raise 'Could not open the I2C bus'


"""
Public Classes
"""


class ADC:

    """
    Based on the Microchip MCP3208
    """

    # variables
    __adcrefvoltage = 4.096  # reference voltage for the ADC chip.

    __spiADC = None

    def __init__(self):
        """
        Define SPI bus and init
        """
        self.__spiADC = spidev.SpiDev()
        self.__spiADC.open(0, 0)
        self.__spiADC.max_speed_hz = (200000)

    # public methods

    def read_adc_voltage(self, channel, mode):
        """
        Read the voltage from the selected channel on the ADC

        :param channel: 1 to 8
        :type channel: int
        :param mode: 0 = single-ended, 1 = differential
        :type mode: int
        :raises ValueError: read_adc_voltage: mode out of range
        :raises ValueError: read_adc_voltage: channel out of range
        :raises ValueError: read_adc_voltage: channel out of range
        :return: voltage
        :rtype: float
        """
        if (mode < 0) or (mode > 1):
            raise ValueError('read_adc_voltage: mode out of range')
        if (channel > 4) and (mode == 1):
            raise ValueError('read_adc_voltage: channel out of range')
        if (channel > 8) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')

        raw = self.read_adc_raw(channel, mode)
        voltage = (self.__adcrefvoltage / 4096) * raw
        return voltage

    def read_adc_raw(self, channel, mode):
        """
        Read the raw value from the selected channel on the ADC

        :param channel: 1 to 8
        :type channel: int
        :param mode: 0 = single-ended, 1 = differential
        :type mode: int
        :raises ValueError: read_adc_voltage: mode out of range
        :raises ValueError: read_adc_voltage: channel out of range
        :raises ValueError: read_adc_voltage: channel out of range
        :return: raw output from ADC
        :rtype: int
        """
        if (mode < 0) or (mode > 1):
            raise ValueError('read_adc_voltage: mode out of range')
        if (channel > 4) and (mode == 1):
            raise ValueError('read_adc_voltage: channel out of range')
        if (channel > 8) or (channel < 1):
            raise ValueError('read_adc_voltage: channel out of range')

        channel = channel - 1
        if mode == 0:
            raw = self.__spiADC.xfer2(
                [6 + (channel >> 2), (channel & 3) << 6, 0])
        if mode == 1:
            raw = self.__spiADC.xfer2(
                [4 + (channel >> 2), (channel & 3) << 6, 0])
        ret = ((raw[1] & 0x0F) << 8) + (raw[2])
        return ret

    def set_adc_refvoltage(self, voltage):
        """
        set the reference voltage for the analogue to digital converter.
        By default, the ADC uses an onboard 4.096V voltage reference.  If you
        choose to use an external voltage reference you will need to
        use this method to set the ADC reference voltage to match the
        supplied reference voltage.
        The reference voltage must be less than or equal to the voltage on
        the Raspberry Pi 5V rail.

        :param voltage: reference voltage
        :type voltage: float
        :raises ValueError: set_adc_refvoltage: reference voltage out of range
        """

        if (voltage >= 0.0) and (voltage <= 5.5):
            self.__adcrefvoltage = voltage
        else:
            raise ValueError('set_adc_refvoltage: reference voltage \
                            out of range')
        return


class DAC:
    """
    Based on the Microchip MCP4822
    """

    __spiDAC = None
    dactx = [0, 0]

    # Max DAC output voltage.  Depends on the gain factor
    # The following table is in the form <gain factor>:<max voltage>
    __dacMaxOutput__ = {
        1: 2.048,  # This is Vref
        2: 4.096  # This is double Vref
    }

    maxdacvoltage = 2.048

    # public methods
    def __init__(self, gainFactor=1):
        """
        Class Constructor - Define SPI bus and init

        :param gainFactor: Set the DAC's gain factor. The value should
           be 1 or 2.  Gain factor is used to determine the output voltage
           from the formula: Vout = G * Vref * D/4096
           Where G is the gain factor, Vref (for this chip) is 2.048 and
           D is the 12-bit digital value, defaults to 1
        :type gainFactor: int, optional
        :raises ValueError: DAC __init__: Invalid gain factor. Must be 1 or 2
        """

        # Define SPI bus and init
        self.__spiDAC = spidev.SpiDev()
        self.__spiDAC.open(0, 1)
        self.__spiDAC.max_speed_hz = (20000000)

        if (gainFactor != 1) and (gainFactor != 2):
            raise ValueError('DAC __init__: Invalid gain factor. \
                            Must be 1 or 2')
        else:
            self.gain = gainFactor

            self.maxdacvoltage = self.__dacMaxOutput__[self.gain]

    def set_dac_voltage(self, channel, voltage):
        """
        Set the voltage for the selected channel on the DAC

        :param channel: 1 or 2
        :type channel: int
        :param voltage: 0 to 2.047 volts when the gain is set to 1
                        or 4.096 when the gain is set to 2
        :type voltage: float
        :raises ValueError: set_dac_voltage: DAC channel needs to be 1 or 2
        :raises ValueError: set_dac_voltage: voltage out of range
        """
        if (channel > 2) or (channel < 1):
            raise ValueError('set_dac_voltage: DAC channel needs to be 1 or 2')
        if (voltage >= 0.0) and (voltage < self.maxdacvoltage):
            rawval = (voltage / 2.048) * 4096 / self.gain
            self.set_dac_raw(channel, int(rawval))
        else:
            raise ValueError('set_dac_voltage: voltage out of range')
        return

    def set_dac_raw(self, channel, value):
        """
        Set the raw value from the selected channel on the DAC

        :param channel: 1 or 2
        :type channel: int
        :param value: 0 to 4095
        :type value: int
        :raises ValueError: set_dac_voltage: DAC channel needs to be 1 or 2
        :raises ValueError: set_dac_voltage: value out of range
        """

        if (channel > 2) or (channel < 1):
            raise ValueError('set_dac_voltage: DAC channel needs to be 1 or 2')
        if (value < 0) and (value > 4095):
            raise ValueError('set_dac_voltage: value out of range')

        self.dactx[1] = (value & 0xff)

        if self.gain == 1:
            self.dactx[0] = (((value >> 8) & 0xff) | (channel - 1) << 7 |
                             1 << 5 | 1 << 4)
        else:
            self.dactx[0] = (((value >> 8) & 0xff) | (channel - 1) << 7 |
                             1 << 4)

        # Write to device
        self.__spiDAC.xfer2(self.dactx)
        return


class IO:

    """
    The MCP23017 chip is split into two 8-bit ports.  port 0 controls pins
    1 to 8 while port 1 controls pins 9 to 16.
    When writing to or reading from a port the least significant bit
    represents the lowest numbered pin on the selected port.
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
    # opposite from the register bit, an interrupt occurs.
    DEFVALA = 0x06

    # Default value for port B - These bits set the compare value for pins
    # configured for interrupt-on-change.  If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALB = 0x07

    # Interrupt control register for port A.
    # If 1, interrupt is fired when the pin matches the default value.
    # If 0, the interrupt is fired on state change.
    INTCONA = 0x08

    # Interrupt control register for port B.
    # If 1 interrupt is fired when the pin matches the default value.
    # If 0 the interrupt is fired on state change.
    # change
    INTCONB = 0x09

    IOCON = 0x0A  # See datasheet for configuration register
    GPPUA = 0x0C  # Pullup resistors for port A
    GPPUB = 0x0D  # Pullup resistors for port B

    # The INTF register reflects the interrupt condition on the port A pins of
    # any pin that is enabled for interrupts. A set bit indicates that the
    # associated pin caused the interrupt trigger.
    INTFA = 0x0E

    # The INTF register reflects the interrupt condition on the port B pins of
    # any pin that is enabled for interrupts.  A set bit indicates that the
    # associated pin caused the interrupt trigger.
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

    __ioaddress = 0x20  # I2C address

    # initial configuration - see IOCON page in the MCP23017 datasheet for
    # more information.
    __ioconfig = 0x02
    __helper = None
    __bus = None

    def __init__(self, initialise=True, bus=None):
        """
        IOPi object initialisation

        :param initialise: True = direction set as inputs, pullups disabled,
                           ports are not inverted.
                           False = device state unaltered. Defaults to True
        :type initialise: bool, optional
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int, optional
        """
        self.__helper = _ABEHelpers()
        self.__bus = self.__helper.get_smbus(bus)
        self.__bus.write_byte_data(self.__ioaddress, self.IOCON,
                                   self.__ioconfig)

        if initialise is True:
            self.__bus.write_word_data(self.__ioaddress, self.IODIRA, 0xFFFF)
            self.__bus.write_word_data(self.__ioaddress, self.GPPUA, 0x0000)
            self.__bus.write_word_data(self.__ioaddress, self.IPOLA, 0x0000)
        return

    # local methods
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
        :param a_register: A register, e.g. IODIRA
        :type a_register: int
        :param b_register: B register, e.g. IODIRB
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
        :param a_register: A register, e.g. IODIRA
        :type a_register: int
        :param b_register: B register, e.g. IODIRB
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
        :param a_register: A register, e.g. IODIRA
        :type a_register: int
        :param b_register: B register, e.g. IODIRB
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
        :param a_register: A register, e.g. IODIRA
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
        :raises ValueError: if pin is out of range, 1 to 16
        :raises ValueError: if value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.IODIRA, self.IODIRB)
        return

    def get_pin_direction(self, pin):
        """
        Get the IO direction for an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: if pin is out of range, 1 to 16
        :return: 1 = input, 0 = output
        :rtype: int
        """
        return self.__get_pin(pin, self.IODIRA, self.IODIRB)

    def set_port_direction(self, port, value):
        """
        Set the direction for an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.IODIRA, self.IODIRB)
        return

    def get_port_direction(self, port):
        """
        Get the direction from an IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.IODIRA, self.IODIRB)

    def set_bus_direction(self, value):
        """
        Set the direction for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.IODIRA)
        return

    def get_bus_direction(self):
        """
        Get the direction for an IO bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = input, 0 = output
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.IODIRA)

    def set_pin_pullup(self, pin, value):
        """
        Set the internal 100K pullup resistors for an individual pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if pin is out of range, 1 to 16
        :raises ValueError: if value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.GPPUA, self.GPPUB)
        return

    def get_pin_pullup(self, pin):
        """
        Get the internal 100K pullup resistors for an individual pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: if pin is out of range, 1 to 16
        :return: 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__get_pin(pin, self.GPPUA, self.GPPUB)

    def set_port_pullups(self, port, value):
        """
        Set the internal 100K pullup resistors for the selected IO port

         :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """
        self.__set_port(port, value, self.GPPUA, self.GPPUB)
        return

    def get_port_pullups(self, port):
        """
        Get the internal pullup status for the selected IO port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.GPPUA, self.GPPUB)

    def set_bus_pullups(self, value):
        """
        Set internal 100K pullup resistors for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPPUA)
        return

    def get_bus_pullups(self):
        """
        Get the internal 100K pullup resistors for an IO bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.GPPUA)

    def write_pin(self, pin, value):
        """
        Write to an individual pin 1 - 16

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if pin is out of range, 1 to 16
        :raises ValueError: if value is out of range, 0 or 1
        """
        self.__set_pin(pin, value, self.GPIOA, self.GPIOB)
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
        self.__set_port(port, value, self.GPIOA, self.GPIOB)
        return

    def write_bus(self, value):
        """
        Write to all pins on the selected bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = logic high, 0 = logic low
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPIOA)
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
        return self.__get_pin(pin, self.GPIOA, self.GPIOB)

    def read_port(self, port):
        """
        Read all pins on the selected port

        :param port: 0 = pins 1 to 8, port 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        """
        return self.__get_port(port, self.GPIOA, self.GPIOB)

    def read_bus(self):
        """
        Read all pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF)
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.GPIOA)

    def invert_pin(self, pin, value):
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

    def get_pin_polarity(self, pin):
        """
        Get the polarity of the selected pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: if pin is out of range, 1 to 16
        :return: 0 = same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__get_pin(pin, self.IPOLA, self.IPOLB)

    def invert_port(self, port, value):
        """
        Invert the polarity of the pins on a selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.IPOLA, self.IPOLB)
        return

    def get_port_polarity(self, port):
        """
        Get the polarity for the selected IO port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.IPOLA, self.IPOLB)

    def invert_bus(self, value):
        """
        Invert the polarity of the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.IPOLA)
        return

    def get_bus_polarity(self):
        """
        Get the polarity of the pins on the bus

        :return: 16-bit number 0 to 65535 (0xFFFF). For each bit
                 0 = same logic state of the input pin,
                 1 = inverted logic state of the input pin
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.IPOLA)

    def mirror_interrupts(self, value):
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

        conf = self.__bus.read_byte_data(self.__ioaddress, self.IOCON)

        if value == 0:
            conf = self.__updatebyte(conf, 6, 0)
            self.__bus.write_byte_data(self.__ioaddress, self.IOCON, conf)
        if value == 1:
            conf = self.__updatebyte(conf, 6, 1)
            self.__bus.write_byte_data(self.__ioaddress, self.IOCON, conf)
        return

    def set_interrupt_polarity(self, value):
        """
        This sets the polarity of the INT output pins

        :param value: 1 = Active-high.  0 = Active-low.
        :type value: int
        :raises ValueError: value out of range: 0 or 1
        """

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        conf = self.__bus.read_byte_data(self.__ioaddress, self.IOCON)

        if value == 0:
            conf = self.__updatebyte(conf, 1, 0)
            self.__bus.write_byte_data(self.__ioaddress, self.IOCON, conf)
        if value == 1:
            conf = self.__updatebyte(conf, 1, 1)
            self.__bus.write_byte_data(self.__ioaddress, self.IOCON, conf)

        return

    def get_interrupt_polarity(self):
        """
        Get the polarity of the INT output pins
        :return: 1 = Active-high.  0 = Active-low.
        :rtype: int
        """
        return self.__checkbit(self.__bus.read_byte_data(self.__ioaddress,
                                                         self.IOCON), 1)

    def set_interrupt_type(self, port, value):
        """
        Sets the type of interrupt for each pin on the selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = interrupt is fired when the pin matches
                      the default value, 0 = interrupt fires on state change
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.INTCONA, self.INTCONB)
        return

    def get_interrupt_type(self, port):
        """
        Get the type of interrupt for each pin on the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: 8-bit number 0 to 255 (0xFF)
                 For each bit 1 = interrupt is fired when the pin matches
                 the default value, 0 = interrupt fires on state change
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.INTCONA, self.INTCONB)

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite of the register bit, an
        interrupt occurs.

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.DEFVALA, self.DEFVALB)
        return

    def get_interrupt_defaults(self, port):
        """
        Get the interrupt default value for each pin on the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: 8-bit number 0 to 255 (0xFF)
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.DEFVALA, self.DEFVALB)

    def set_interrupt_on_pin(self, pin, value):
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

    def get_interrupt_on_pin(self, pin):
        """
        Gets whether the interrupt is enabled for the selected pin

        :param pin: pin to read, 1 to 16
        :type pin: int
        :raises ValueError: if pin is out of range, 1 to 16
        :return: 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__get_pin(pin, self.GPINTENA, self.GPINTENB)

    def set_interrupt_on_port(self, port, value):
        """
        Enable interrupts for the pins on the selected port

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value is out of range, 0 to 0xFF
        """
        self.__set_port(port, value, self.GPINTENA, self.GPINTENB)
        return

    def get_interrupt_on_port(self, port):
        """
        Gets whether the interrupts are enabled for the selected port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        return self.__get_port(port, self.GPINTENA, self.GPINTENB)

    def set_interrupt_on_bus(self, value):
        """
        Enable interrupts for the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """
        self.__set_bus(value, self.GPINTENA)
        return

    def get_interrupt_on_bus(self):
        """
        Gets whether the interrupts are enabled for the bus

        :return: 16-bit number 0 to 65535 (0xFFFF).
                 For each bit 1 = enabled, 0 = disabled
        :rtype: int
        """
        return self.__bus.read_word_data(self.__ioaddress, self.GPINTENA)

    def read_interrupt_status(self, port):
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

    def read_interrupt_capture(self, port):
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

    def reset_interrupts(self):
        """
        Reset the interrupts A and B to 0
        """
        tmp = self.read_interrupt_capture(0)
        tmp = self.read_interrupt_capture(1)
        del tmp
        return


class RTC:
    """
    Based on the Maxim DS1307
    """
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYOFWEEK = 0x03
    DAY = 0x04
    MONTH = 0x05
    YEAR = 0x06
    CONTROL = 0x07

    # variables
    __rtcaddress = 0x68  # I2C address
    # initial configuration - square wave and output disabled, frequency set
    # to 32.768KHz.
    __rtcconfig = 0x03
    # the DS1307 does not store the current century so that has to be added on
    # manually.
    __century = 2000

    __helper = None
    __bus = None

    # local methods

    def __init__(self, bus=None):
        """
        Initialise the RTC module
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int, optional
        """
        self.__helper = _ABEHelpers()
        self.__bus = self.__helper.get_smbus(bus)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

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
        Internal method for converting a decimal formatted number to BCD

        :param dec: decimal number
        :type dec: int
        :return: BCD formatted number
        :rtype: int
        """
        bcd = 0
        for vala in (dec // 10, dec % 10):
            for valb in (8, 4, 2, 1):
                if vala >= valb:
                    bcd += 1
                    vala -= valb
                bcd <<= 1
        return bcd >> 1

    def __get_century(self, val):
        """
        Internal method for storing the current century

        :param val: year
        :type val: int
        """
        if len(val) > 2:
            year = val[0] + val[1]
            self.__century = int(year) * 100
        return

    # public methods
    def set_date(self, date):
        """
        Set the date and time on the RTC

        :param date: ISO 8601 formatted string - "YYYY-MM-DDTHH:MM:SS"
        :type date: string
        """
        newdate = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        self.__get_century(date)
        writeval = [self.__dec_bcd(newdate.second),
                    self.__dec_bcd(newdate.minute),
                    self.__dec_bcd(newdate.hour),
                    self.__dec_bcd(newdate.weekday()),
                    self.__dec_bcd(newdate.day),
                    self.__dec_bcd(newdate.month),
                    self.__dec_bcd(newdate.year - self.__century)]

        self.__bus.write_i2c_block_data(self.__rtcaddress, 0x00, writeval)

        return

    def read_date(self):
        """
        Read the date and time from the RTC

        :return: ISO 8601 formatted string - "YYYY-MM-DDTHH:MM:SS"
        :rtype: string
        """
        readval = self.__bus.read_i2c_block_data(self.__rtcaddress, 0, 7)
        date = ("%02d-%02d-%02dT%02d:%02d:%02d" % (self.__bcd_dec(readval[6]) +
                                                   self.__century,
                                                   self.__bcd_dec(readval[5]),
                                                   self.__bcd_dec(readval[4]),
                                                   self.__bcd_dec(readval[2]),
                                                   self.__bcd_dec(readval[1]),
                                                   self.__bcd_dec(readval[0])))
        return date

    def enable_output(self):
        """
        Enable the output pin
        """

        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 7, 1)
        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 4, 1)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 7, 0)
        self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 4, 0)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
        return

    def set_frequency(self, frequency):
        """
        Set the frequency of the output pin square-wave

        :param frequency: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        :type frequency: int
        """

        if frequency == 1:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 2:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 0)
        if frequency == 3:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 0)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 1)
        if frequency == 4:
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 0, 1)
            self.__rtcconfig = self.__helper.updatebyte(self.__rtcconfig, 1, 1)
        self.__bus.write_byte_data(
            self.__rtcaddress, self.CONTROL, self.__rtcconfig)
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

        if address >= 0x08 and address <= 0x3F:
            if address + len(valuearray) <= 0x3F:
                self.__bus.write_i2c_block_data(
                    self.__rtcaddress, address, valuearray)
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

        if address >= 0x08 and address <= 0x3F:
            if address <= (0x3F - length):
                return self.__bus.read_i2c_block_data(self.__rtcaddress,
                                                      address, length)
            else:
                raise ValueError('read_memory: memory overflow error: address + \
                                length exceeds 0x3F')
        else:
            raise ValueError('read_memory: address out of range')
