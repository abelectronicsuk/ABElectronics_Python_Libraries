#!/usr/bin/python

"""
 ================================================
 ABElectronics IO Pi 32-Channel Port Expander
 Version 1.0 Created 30/04/2014
 Version 1.1 bug fixes
 Version 1.2 changes to format source code to PEP8 rules 12/11/2014

Requires python 2 smbus to be installed with: sudo apt-get install python-smbus
================================================


Each MCP23017 chip is split into two 8-bit ports.  port 0 controls
pins 1 to 8 while port 1 controls pins 9 to 16.
When writing to or reading from a port the least significant bit represents
the lowest numbered pin on the selected port.
"""


class IoPi(object):
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
    # configured for interrupt-on-change. If the associated pin level is the
    # opposite from the register bit, an interrupt occurs.
    DEFVALA = 0x06
    # Default value for port B - These bits set the compare value for pins
    # configured for interrupt-on-change. If the associated pin level is the
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
    # any pin that is enabled for interrupts. A set bit indicates that the
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
    address = 0x20  # I2C address
    port_a_dir = 0x00  # port a direction
    port_b_dir = 0x00  # port b direction
    portaval = 0x00  # port a value
    portbval = 0x00  # port b value
    porta_pullup = 0x00  # port a pull-up resistors
    portb_pullup = 0x00  # port a pull-up resistors
    porta_polarity = 0x00  # input polarity for port a
    portb_polarity = 0x00  # input polarity for port b
    intA = 0x00  # interrupt control for port a
    intB = 0x00  # interrupt control for port a
    # initial configuration - see IOCON page in the MCP23017 datasheet for
    # more information.
    config = 0x22
    global _bus

    def __init__(self, bus, address=0x20):
        """
        init object with smbus object, i2c address, default is 0x20, 0x21 for
        IOPi board,
        Load default configuration, all pins are inputs with pull-ups disabled
        """
        self._bus = bus
        self.address = address
        self._bus.write_byte_data(self.address, self.IOCON, self.config)
        self.portaval = self._bus.read_byte_data(self.address, self.GPIOA)
        self.portbval = self._bus.read_byte_data(self.address, self.GPIOB)        
        self._bus.write_byte_data(self.address, self.IODIRA, 0xFF)
        self._bus.write_byte_data(self.address, self.IODIRB, 0xFF)
        self.set_port_pullups(0,0x00)
        self.set_port_pullups(1,0x00)
        self.invert_port(0, 0x00)
        self.invert_port(1, 0x00)
        return

    # local methods

    def __updatebyte(self, byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """
        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    def __checkbit(self, byte, bit):
        """
         internal method for reading the value of a single bit within a byte
        """
        if byte & (1 << bit):
            return 1
        else:
            return 0

    # public methods

    def set_pin_direction(self, pin, direction):
        """
         set IO direction for an individual pin
         pins 1 to 16
         direction 1 = input, 0 = output
         """
        pin = pin - 1
        if pin < 8:
            self.port_a_dir = self.__updatebyte(self.port_a_dir, pin, direction)
            self._bus.write_byte_data(self.address, self.IODIRA, self.port_a_dir)
        else:
            self.port_b_dir  = self.__updatebyte(self.port_b_dir, pin - 8, direction)
            self._bus.write_byte_data(self.address, self.IODIRB, self.port_b_dir)
        return

    def set_port_direction(self, port, direction):
        """
        set direction for an IO port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        1 = input, 0 = output
        """
        if port == 1:
            self._bus.write_byte_data(self.address, self.IODIRB, direction)
            self.port_b_dir = direction
        else:
            self._bus.write_byte_data(self.address, self.IODIRA, direction)
            self.port_a_dir = direction
        return

    def set_pin_pullup(self, pinval, value):
        """
        set the internal 100K pull-up resistors for an individual pin
        pins 1 to 16
        value 1 = enabled, 0 = disabled
        """
        pin = pinval - 1
        if pin < 8:
            self.porta_pullup = self.__updatebyte(self.porta_pullup, pin, value)
            self._bus.write_byte_data(self.address, self.GPPUA, self.porta_pullup)
        else:
            self.portb_pullup = self.__updatebyte(self.portb_pullup,pin - 8,value)
            self._bus.write_byte_data(self.address, self.GPPUB, self.portb_pullup)
        return

    def set_port_pullups(self, port, value):
        """
        set the internal 100K pull-up resistors for the selected IO port
        """
        if port == 1:
            self.portb_pullup = value
            self._bus.write_byte_data(self.address, self.GPPUB, value)
        else:
            self.porta_pullup = value
            self._bus.write_byte_data(self.address, self.GPPUA, value)
        return

    def write_pin(self, pin, value):
        """
        write to an individual pin 1 - 16
        """
        pin = pin - 1
        if pin < 8:
            self.portaval = self.__updatebyte(self.portaval, pin, value)
            self._bus.write_byte_data(self.address, self.GPIOA, self.portaval)
        else:
            self.portbval = self.__updatebyte(self.portbval, pin - 8, value)
            self._bus.write_byte_data(self.address, self.GPIOB, self.portbval)
        return

    def write_port(self, port, value):
        """
        write to all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """
        if port == 1:
            self._bus.write_byte_data(self.address, self.GPIOB, value)
            self.portbval = value
        else:
            self._bus.write_byte_data(self.address, self.GPIOA, value)
            self.portaval = value
        return

    def read_pin(self, pinval):
        """
        read the value of an individual pin 1 - 16
        returns 0 = logic level low, 1 = logic level high
        """
        pin = pinval - 1
        if pin < 8:
            self.portaval = self._bus.read_byte_data(self.address, self.GPIOA)
            return self.__checkbit(self.portaval, pin)
        else:
            pin = pin - 8
            self.portbval = self._bus.read_byte_data(self.address, self.GPIOB)
            return self.__checkbit(self.portbval, pin)

    def read_port(self, port):
        """
        read all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        returns number between 0 and 255 or 0x00 and 0xFF
        """
        if port == 1:
            self.portbval = self._bus.read_byte_data(self.address, self.GPIOB)
            return self.portbval
        else:
            self.portaval = self._bus.read_byte_data(self.address, self.GPIOA)
            return self.portaval

    def invert_port(self, port, polarity):
        """
        invert the polarity of the pins on a selected port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """
        if port == 1:
            self._bus.write_byte_data(self.address, self.IPOLB, polarity)
            self.portb_polarity = polarity
        else:
            self._bus.write_byte_data(self.address, self.IPOLA, polarity)
            self.porta_polarity = polarity
        return

    def invert_pin(self, pin, polarity):
        """
        invert the polarity of the selected pin
        pins 1 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """
        pin = pin - 1
        if pin < 8:
            self.porta_polarity = self.__updatebyte(
                self.porta_polarity,
                pin,
                polarity)
            self._bus.write_byte_data(self.address, self.IPOLA, self.porta_polarity)
        else:
            self.portb_polarity = self.__updatebyte(
                self.portb_polarity,
                pin -
                8,
                polarity)
            self._bus.write_byte_data(self.address, self.IPOLB, self.portb_polarity)
        return

    def mirror_interrupts(self, value):
        """
        1 = The INT pins are internally connected, 0 = The INT pins are not
        connected. INTA is associated with PortA and INTB is associated with
        PortB
        """
        if value == 0:
            self.config = self.__updatebyte(self.config, 6, 0)
            self._bus.write_byte_data(self.address, self.IOCON, self.config)
        if value == 1:
            self.config = self.__updatebyte(self.config, 6, 1)
            self._bus.write_byte_data(self.address, self.IOCON, self.config)
        return

    def set_interrupt_polarity(self, value):
        """
        This sets the polarity of the INT output pins - 1 = Active-high.
        0 = Active-low.
        """
        if value == 0:
            self.config = self.__updatebyte(self.config, 1, 0)
            self._bus.write_byte_data(self.address, self.IOCON, self.config)
        if value == 1:
            self.config = self.__updatebyte(self.config, 1, 1)
            self._bus.write_byte_data(self.address, self.IOCON, self.config)
        return
        return

    def set_interrupt_type(self, port, value):
        """
        Sets the type of interrupt for each pin on the selected port
        1 = interrupt is fired when the pin matches the default value
        0 = the interrupt is fired on state change
        """
        if port == 0:
            self._bus.write_byte_data(self.address, self.INTCONA, value)
        else:
            self._bus.write_byte_data(self.address, self.INTCONB, value)
        return

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite from the register bit, an
        interrupt occurs.
        """
        if port == 0:
            self._bus.write_byte_data(self.address, self.DEFVALA, value)
        else:
            self._bus.write_byte_data(self.address, self.DEFVALB, value)
        return

    def set_interrupt_on_port(self, port, value):
        """
        Enable interrupts for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """
        if port == 0:
            self._bus.write_byte_data(self.address, self.GPINTENA, value)
            self.intA = value
        else:
            self._bus.write_byte_data(self.address, self.GPINTENB, value)
            self.intB = value
        return

    def set_interrupt_on_pin(self, pin, value):
        """
        Enable interrupts for the selected pin
        Pin = 1 to 16
        Value 0 = interrupt disabled, 1 = interrupt enabled
        """
        pin = pin - 1
        if pin < 8:
            self.intA = self.__updatebyte(self.intA, pin, value)
            self._bus.write_byte_data(self.address, self.GPINTENA, self.intA)
        else:
            self.intB = self.__updatebyte(self.intB, pin - 8, value)
            self._bus.write_byte_data(self.address, self.GPINTENB, self.intB)
        return

    def read_interrupt_status(self, port):
        """
        read the interrupt status for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        """
        if port == 0:
            return self._bus.read_byte_data(self.address, self.INTFA)
        else:
            return self._bus.read_byte_data(self.address, self.INTFB)

    def read_interrupt_capture(self, port):
        """
        read the value from the selected port at the time of the last
        interrupt trigger
        port 0 = pins 1 to 8, port 1 = pins 8 to 16
        """
        if port == 0:
            return self._bus.read_byte_data(self.address, self.INTCAPA)
        else:
            return self._bus.read_byte_data(self.address, self.INTCAPB)

    def reset_interrupts(self):
        """
        set the interrupts A and B to 0
        """
        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return
