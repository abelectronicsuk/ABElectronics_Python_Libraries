#!/usr/bin/env python
"""
 ================================================
 ABElectronics IO Pi 32-Channel Port Expander

Requires smbus2 or python smbus to be installed
================================================


Each MCP23017 chip is split into two 8-bit ports.  Port 0 controls
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


class IOPi(object):
    """
    The MCP23017 chip is split into two 8-bit ports.  Port 0 controls pins
    1 to 8 while Port 1 controls pins 9 to 16.
    When writing to or reading from a bus or port the least significant bit
    represents the lowest numbered pin on the selected port.
    #
    """

    # Define registers values from datasheet
    IODIRA = 0x00  # IO direction A - 1= input 0 = output
    IODIRB = 0x01  # IO direction B - 1= input 0 = output
    # Input polarity A - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLA = 0x02
    # Input polarity B - If a bit is set, the corresponding GPIO register bit
    # will reflect the inverted value on the pin.
    IPOLB = 0x03
    # The GPINTEN register controls the interrupt-onchange feature for each
    # pin on port A.
    GPINTENA = 0x04
    # The GPINTEN register controls the interrupt-onchange feature for each
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
    # Interrupt control register for port A.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONA = 0x08
    # Interrupt control register for port B.  If 1 interrupt is fired when the
    # pin matches the default value, if 0 the interrupt is fired on state
    # change
    INTCONB = 0x09
    IOCON = 0x0A  # see datasheet for configuration register
    GPPUA = 0x0C  # pull-up resistors for port A
    GPPUB = 0x0D  # pull-up resistors for port B
    # The INTF register reflects the interrupt condition on the port A pins of
    # any pin that is enabled for interrupts. A set bit indicates that the
    # associated pin caused the interrupt.
    INTFA = 0x0E
    # The INTF register reflects the interrupt condition on the port B pins of
    # any pin that is enabled for interrupts.  A set bit indicates that the
    # associated pin caused the interrupt.
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
    __ioaddress = 0x20  # I2C address
    # initial configuration
    # see IOCON page in the MCP23017 datasheet for more information.
    __conf = 0x02
    __helper = None
    __bus = None

    def __init__(self, address, initialise=True):
        """
        IOPi object initialisation

        :param address: i2c address for the target device, 0x20 to 0x27
        :type address: int
        :param initialise: True = direction set as inputs, pull-ups disabled,
                           ports not inverted.
                           False = device state unaltered., defaults to True
        :type initialise: bool, optional
        """

        if address < 0x20 or address > 0x27:
            raise ValueError("__init__ i2c address out of range: 0x20 to 0x27")
        if type(initialise) is not bool:
            raise ValueError("__init__ initialise must be bool: True of False")

        self.__ioaddress = address
        self.__bus = self.__get_smbus()
        self.__bus.write_byte_data(self.__ioaddress, self.IOCON, self.__conf)

        if initialise is True:
            self.__bus.write_word_data(self.__ioaddress, self.IODIRA, 0xFFFF)
            self.__bus.write_word_data(self.__ioaddress, self.GPPUA, 0x0000)
            self.__bus.write_word_data(self.__ioaddress, self.IPOLA, 0x0000)
        return

    # local methods
    @staticmethod
    def __get_smbus():
        """
        Internal method for getting an instance of the i2c bus

        :return: i2c bus for target device
        :rtype: SMBus
        :raises IOError: Could not open the i2c bus
        """
        i2c__bus = 1
        # detect the device that is being used
        device = platform.uname()[1]

        if device == "orangepione":  # running on orange pi one
            i2c__bus = 0

        elif device == "orangepiplus":  # running on orange pi plus
            i2c__bus = 0

        elif device == "orangepipcplus":  # running on orange pi pc plus
            i2c__bus = 0

        elif device == "linaro-alip":  # running on Asus Tinker Board
            i2c__bus = 1

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
        :return: value of selected bit, 0 or 1
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

    # public methods

    def set_pin_direction(self, pin, value):
        """
        Set IO direction for an individual pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = input, 0 = output
        :type value: int
        :raises ValueError: if pin is out of range, 1 to 16
        :raises ValueError: if value is out of range, 0 or 1
        """

        reg = None
        if pin >= 1 and pin <= 8:
            reg = self.IODIRA
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = self.IODIRB
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

        return

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.IODIRA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.IODIRB, value)
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
        if port == 0:
            return self.__bus.read_byte_data(self.__ioaddress, self.IODIRA)
        elif port == 1:
            return self.__bus.read_byte_data(self.__ioaddress, self.IODIRB)
        else:
            raise ValueError("port out of range: 0 or 1")
        return

    def set_bus_direction(self, value):
        """
        Set direction for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = input, 0 = output
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """

        if value >= 0x0000 and value <= 0xFFFF:
            self.__bus.write_word_data(self.__ioaddress, self.IODIRA, value)
        else:
            raise ValueError('value out of range: 0 to 65535 (0xFFFF)')
        return

    def set_pin_pullup(self, pin, value):
        """
        Set the internal 100K pull-up resistors for an individual pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if pin is out of range, 1 to 16
        :raises ValueError: if value is out of range, 0 or 1
        """

        reg = None
        if pin >= 1 and pin <= 8:
            reg = self.GPPUA
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = self.GPPUB
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

        return

    def set_port_pullups(self, port, value):
        """
        Set the internal 100K pull-up resistors for the selected IO port

         :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: value out of range: 0 to 255 (0xFF)
        """

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPPUB, value)
        return

    def get_port_pullups(self, port):
        """
        Get the internal pull-up status for the selected IO port
        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        :raises ValueError: if port is out of range, 0 or 1
        """
        if port == 0:
            return self.__bus.read_byte_data(self.__ioaddress, self.GPPUA)
        elif port == 1:
            return self.__bus.read_byte_data(self.__ioaddress, self.GPPUB)
        else:
            raise ValueError("port out of range: 0 or 1")
        return

    def set_bus_pullups(self, value):
        """
        Set internal 100K pull-up resistors for an IO bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """

        if value >= 0x0000 and value <= 0xFFFF:
            self.__bus.write_word_data(self.__ioaddress, self.GPPUA, value)
        else:
            raise ValueError('value out of range: 0 to 65535 (0xFFFF)')
        return

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

        reg = None
        if pin >= 1 and pin <= 8:
            reg = self.GPIOA
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = self.GPIOB
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPIOB, value)
        return

    def write_bus(self, value):
        """
        Write to all pins on the selected bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = logic high, 0 = logic low
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """

        if value >= 0x0000 and value <= 0xFFFF:
            self.__bus.write_word_data(self.__ioaddress, self.GPIOA, value)
        else:
            raise ValueError('value out of range: 0 to 65535 (0xFFFF)')
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

        value = 0

        if pin >= 1 and pin <= 8:
            curval = self.__bus.read_byte_data(self.__ioaddress, self.GPIOA)
            value = self.__checkbit(curval, pin - 1)
        elif pin >= 9 and pin <= 16:
            curval = self.__bus.read_byte_data(self.__ioaddress, self.GPIOB)
            value = self.__checkbit(curval, pin - 9)
        else:
            raise ValueError("pin out of range: 1 to 16")

        return value

    def read_port(self, port):
        """
        Read all pins on the selected port

        :param port: 0 = pins 1 to 8, port 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: number between 0 and 255 (0xFF)
        :rtype: int
        """

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if port == 0:
            return self.__bus.read_byte_data(self.__ioaddress, self.GPIOA)
        else:
            return self.__bus.read_byte_data(self.__ioaddress, self.GPIOB)

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
        pins 1 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin

        :param pin: pin to update, 1 to 16
        :type pin: int
        :param value: 0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: pin out of range: 1 to 16
        :raises ValueError: polarity out of range: 0 or 1
        """

        reg = None
        if pin >= 1 and pin <= 8:
            reg = self.IPOLA
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = self.IPOLB
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("polarity out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

        return

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.IPOLB, value)
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
        if port == 0:
            return self.__bus.read_byte_data(self.__ioaddress, self.IPOLA)
        elif port == 1:
            return self.__bus.read_byte_data(self.__ioaddress, self.IPOLB)
        else:
            raise ValueError("port out of range: 0 or 1")
        return

    def invert_bus(self, value):
        """
        Invert the polarity of the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).  For each bit
                      0 = same logic state of the input pin,
                      1 = inverted logic state of the input pin
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """

        if value < 0 or value > 0xFFFF:
            raise ValueError("if value is out of range, 0 to 65535 (0xFFFF)")

        self.__bus.write_word_data(self.__ioaddress, self.IPOLA, value)
        return

    def mirror_interrupts(self, value):
        """
        Sets whether the interrupt pins INT A and INT B are independently
        connected to each port or internally connected together

        :param value: 1 = The INT pins are internally connected,
                      0 = The INT pins are not connected.
                      INT A is associated with PortA and
                      INT B is associated with PortB
        :type value: int
        :raises ValueError: value out of range: 0 or 1
        """

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        if value == 0:
            self.__conf = self.__updatebyte(self.__conf, 6, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__conf)
        if value == 1:
            self.__conf = self.__updatebyte(self.__conf, 6, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__conf)
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

        if value == 0:
            self.__conf = self.__updatebyte(self.__conf, 1, 0)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__conf)
        if value == 1:
            self.__conf = self.__updatebyte(self.__conf, 1, 1)
            self.__bus.write_byte_data(
                self.__ioaddress, self.IOCON, self.__conf)
        return

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.INTCONB, value)
        return

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite from the register bit, an
        interrupt occurs.

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :param value: 8-bit number 0 to 255 (0xFF)
        :type value: int
        :raises ValueError: if port is out of range, 0 or 1
        :raises ValueError: if value is out of range, 0 to 0xFF
        """

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.DEFVALB, value)
        return

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

        reg = None
        if pin >= 1 and pin <= 8:
            reg = self.GPINTENA
            pin = pin - 1
        elif pin >= 9 and pin <= 16:
            reg = self.GPINTENB
            pin = pin - 9
        else:
            raise ValueError("pin out of range: 1 to 16")

        if value < 0 or value > 1:
            raise ValueError("value out of range: 0 or 1")

        curval = self.__bus.read_byte_data(self.__ioaddress, reg)
        newval = self.__updatebyte(curval, pin, value)
        self.__bus.write_byte_data(self.__ioaddress, reg, newval)

        return

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        if value < 0 or value > 0xFF:
            raise ValueError("value out of range: 0 to 255 (0xFF)")

        if port == 0:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENA, value)
        else:
            self.__bus.write_byte_data(self.__ioaddress, self.GPINTENB, value)
        return

    def set_interrupt_on_bus(self, value):
        """
        Enable interrupts for the pins on the bus

        :param value: 16-bit number 0 to 65535 (0xFFFF).
                      For each bit 1 = enabled, 0 = disabled
        :type value: int
        :raises ValueError: if value is out of range, 0 to 65535 (0xFFFF)
        """

        if value < 0 or value > 0xFFFF:
            raise ValueError("if value is out of range, 0 to 65535 (0xFFFF)")

        self.__bus.write_word_data(self.__ioaddress, self.GPINTENA, value)
        return

    def read_interrupt_status(self, port):
        """
        Read the interrupt status for the pins on the selected port
        interrupt trigger

        :param port: 0 = pins 1 to 8, 1 = pins 9 to 16
        :type port: int
        :raises ValueError: port out of range: 0 or 1
        :return: interrupt status for selected port
        :rtype: int
        """

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTFB)
        return value

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

        if port < 0 or port > 1:
            raise ValueError("port out of range: 0 or 1")

        value = 0
        if port == 0:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPA)
        else:
            value = self.__bus.read_byte_data(self.__ioaddress, self.INTCAPB)
        return value

    def reset_interrupts(self):
        """
        Reset the interrupts A and B to 0
        """
        tmp = self.read_interrupt_capture(0)
        tmp = self.read_interrupt_capture(1)
        del tmp
        return
