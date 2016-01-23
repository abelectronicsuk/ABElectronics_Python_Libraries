#!/usr/bin/python

import spidev
import time
import datetime
import sys
import math
import struct

"""
================================================
ABElectronics IO Pi V2 32-Channel Port Expander
Version 1.0 Created 20/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed

================================================
"""




class ADC:

    """
    Based on the Microchip MCP3208
    """

    # variables
    __adcrefvoltage = 4.096  # reference voltage for the ADC chip.

    # Define SPI bus and init
    __spiADC = spidev.SpiDev()
    __spiADC.open(0, 0)
    __spiADC.max_speed_hz = (50000)

    # public methods

    def read_adc_voltage(self, channel):
        """
        Read the voltage from the selected channel on the ADC
        Channel = 1 to 8
        """

        if ((channel > 8) or (channel < 1)):
            print 'ADC channel needs to be 1 to 8'
        raw = self.readADCraw(channel)
        voltage = (self.__adcrefvoltage / 4096) * raw
        return voltage

    def readADCraw(self, channel):
        """
        Read the raw value from the selected channel on the ADC
        Channel = 1 to 8
        """

        if ((channel > 8) or (channel < 1)):
            print 'ADC channel needs to be 1 to 8'
            return 0.0
        channel = channel - 1
        r = self.__spiADC.xfer2([4 + (channel >> 2), (channel & 3) << 6, 0])
        ret = ((r[1] & 0x0F) << 8) + (r[2])
        return ret

    def set_adc_refvoltage(self, voltage):
        """
        set the reference voltage for the analogue to digital converter.
        By default the ADC uses an onboard 4.096V voltage reference.  If you
        choose to use an external voltage reference you will need to
        use this method to set the ADC reference voltage to match the
        supplied reference voltage.
        The reference voltage must be less than or equal to the voltage on
        the Raspberry Pi 5V rail.
        """

        if (voltage >= 0.0) and (voltage <= 5.5):
            self.__adcrefvoltage = voltage
        else:
            print 'reference voltage out of range'
        return


class DAC:

    """
    Based on the Microchip MCP4822


    Define SPI bus and init
    """
    __spiDAC = spidev.SpiDev()
    __spiDAC.open(0, 1)
    __spiDAC.max_speed_hz = (4000000)

    def set_dac_voltage(self, channel, voltage):
        """
        set the voltage for the selected channel on the DAC
        voltage can be between 0 and 2.047 volts
        """

        if ((channel > 2) or (channel < 1)):
            print 'DAC channel needs to be 1 or 2'
        if (voltage >= 0.0) and (voltage < 2.048):
            rawval = (voltage / 2.048) * 4096
            self.set_dac_raw(channel, int(rawval))
        return

    def set_dac_raw(self, channel, value):
        """
        Set the raw value from the selected channel on the DAC
        Channel = 1 or 2
        Value between 0 and 4095
        """

        lowByte = value & 0xff
        highByte = (
            (value >> 8) & 0xff) | (
            channel -
            1) << 7 | 0x1 << 5 | 1 << 4
        self.__spiDAC.xfer2([highByte, lowByte])
        return


class IO:

    """
    The MCP23017 chip is split into two 8-bit ports.  port 0 controls pins
    1 to 8 while port 1 controls pins 9 to 16.
    When writing to or reading from a port the least significant bit
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
    __ioaddress = 0x20  # I2C address
    __portA_dir = 0x00  # port a direction
    __portB_dir = 0x00  # port b direction
    __portA_val = 0x00  # port a value
    __portB_val = 0x00  # port b value
    __portA_pullup = 0x00  # port a pull-up resistors
    __portB_pullup = 0x00  # port a pull-up resistors
    __portA_polarity = 0x00  # input polarity for port a
    __portB_polarity = 0x00  # input polarity for port b
    __intA = 0x00  # interrupt control for port a
    __intB = 0x00  # interrupt control for port a
    # initial configuration - see IOCON page in the MCP23017 datasheet for
    # more information.
    __ioconfig = 0x22
    global _bus

    def __init__(self, bus):
        """
        init object with i2c address, default is 0x20, 0x21 for IOPi board,
        load default configuration
        """
        self._bus = bus
        self._bus.write_byte_data(self.__ioaddress, self.IOCON, self.__ioconfig)
        self.__portA_val = self._bus.read_byte_data(self.__ioaddress, self.GPIOA)
        self.__portB_val = self._bus.read_byte_data(self.__ioaddress, self.GPIOB)
        self._bus.write_byte_data(self.__ioaddress, self.IODIRA, 0xFF)
        self._bus.write_byte_data(self.__ioaddress, self.IODIRB, 0xFF)
        return

    # local methods

    def __updatebyte(self, byte, bit, value):
        """ internal method for setting the value of a single bit
        within a byte """

        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    def __checkbit(self, byte, bit):
        """ internal method for reading the value of a single bit
        within a byte """

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
            self.__portA_dir = self.__updatebyte(self.__portA_dir, pin, direction)
            self._bus.write_byte_data(self.address, self.IODIRA, self.__portA_dir)
        else:
            self.__portB_dir  = self.__updatebyte(self.__portB_dir, pin - 8, direction)
            self._bus.write_byte_data(self.address, self.IODIRB, self.__portB_dir)
        return

    def set_port_direction(self, port, direction):
        """
        set direction for an IO port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        1 = input, 0 = output
        """

        if port == 1:
            self._bus.write_byte_data(self.__ioaddress, self.IODIRB, direction)
            self.__portB_dir = direction
        else:
            self._bus.write_byte_data(self.__ioaddress, self.IODIRA, direction)
            self.__portA_dir = direction
        return

    def set_pin_pullup(self, pin, value):
        """
        set the internal 100K pull-up resistors for an individual pin
        pins 1 to 16
        value 1 = enabled, 0 = disabled
        """
        pin = pin - 1
        if pin < 8:
            self.__portA_pullup = self.__updatebyte(self.__portA_pullup, pin, value)
            self._bus.write_byte_data(self.address, self.GPPUA, self.__portA_pullup)
        else:
            self.__portB_pullup = self.__updatebyte(self.__portB_pullup,pin - 8,value)
            self._bus.write_byte_data(self.address, self.GPPUB, self.__portB_pullup)
        return

    def set_port_pullups(self, port, value):
        """
        set the internal 100K pull-up resistors for the selected IO port
        """

        if port == 1:
            self.__portA_pullup = value
            self._bus.write_byte_data(self.__ioaddress, self.GPPUB, value)
        else:
            self.__portB_pullup = value
            self._bus.write_byte_data(self.__ioaddress, self.GPPUA, value)
        return

    def write_pin(self, pin, value):
        """
        write to an individual pin 1 - 16
        """

        pin = pin - 1
        if pin < 8:
            self.__portA_val = self.__updatebyte(self.__portA_val, pin, value)
            self._bus.write_byte_data(
                self.__ioaddress,
                self.GPIOA,
                self.__portA_val)
        else:
            self.__portB_val = self.__updatebyte(
                self.__portB_val,
                pin -
                8,
                value)
            self._bus.write_byte_data(
                self.__ioaddress,
                self.GPIOB,
                self.__portB_val)
        return

    def write_port(self, port, value):
        """
        write to all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 1:
            self._bus.write_byte_data(self.__ioaddress, self.GPIOB, value)
            self.__portB_val = value
        else:
            self._bus.write_byte_data(self.__ioaddress, self.GPIOA, value)
            self.__portA_val = value
        return

    def read_pin(self, pin):
        """
        read the value of an individual pin 1 - 16
        returns 0 = logic level low, 1 = logic level high
        """

        pin = pin - 1
        if pin < 8:
            self.__portA_val =self._bus.read_byte_data(
                self.__ioaddress,
                self.GPIOA)
            return self.__checkbit(self.__portA_val, pin)
        else:
            pin = pin - 8
            self.__portB_val =self._bus.read_byte_data(
                self.__ioaddress,
                self.GPIOB)
            return self.__checkbit(self.__portB_val, pin)

    def read_port(self, port):
        """
        read all pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        returns number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 1:
            self.__portB_val =self._bus.read_byte_data(
                self.__ioaddress,
                self.GPIOB)
            return self.__portB_val
        else:
            self.__portA_val =self._bus.read_byte_data(
                self.__ioaddress,
                self.GPIOA)
            return self.__portA_val

    def invert_port(self, port, polarity):
        """
        invert the polarity of the pins on a selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        polarity 0 = same logic state of the input pin, 1 = inverted logic
        state of the input pin
        """

        if port == 1:
            self._bus.write_byte_data(self.__ioaddress, self.IPOLB, polarity)
            self.__portB_polarity = polarity
        else:
            self._bus.write_byte_data(self.__ioaddress, self.IPOLA, polarity)
            self.__portA_polarity = polarity
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
            self.__portA_polarity = self.__updatebyte(
                self.__portA_val,
                pin,
                polarity)
            self._bus.write_byte_data(
                self.__ioaddress,
                self.IPOLA,
                self.__portA_polarity)
        else:
            self.__portB_polarity = self.__updatebyte(
                self.__portB_val,
                pin -
                8,
                polarity)
            self._bus.write_byte_data(
                self.__ioaddress,
                self.IPOLB,
                self.__portB_polarity)
        return

    def mirror_interrupts(self, value):
        """
        1 = The INT pins are internally connected, 0 = The INT pins are not
        connected. __intA is associated with PortA and __intB is associated
        with PortB
        """

        if value == 0:
            self.config = self.__updatebyte(self.__ioconfig, 6, 0)
            self._bus.write_byte_data(self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.config = self.__updatebyte(self.__ioconfig, 6, 1)
            self._bus.write_byte_data(self.__ioaddress, self.IOCON, self.__ioconfig)
        return

    def set_interrupt_polarity(self, value):
        """
        This sets the polarity of the INT output pins - 1 = Active-high. 0 =
        Active-low.
        """

        if value == 0:
            self.config = self.__updatebyte(self.__ioconfig, 1, 0)
            self._bus.write_byte_data(self.__ioaddress, self.IOCON, self.__ioconfig)
        if value == 1:
            self.config = self.__updatebyte(self.__ioconfig, 1, 1)
            self._bus.write_byte_data(self.__ioaddress, self.IOCON, self.__ioconfig)
        return
        return

    def set_interrupt_type(self, port, value):
        """
        Sets the type of interrupt for each pin on the selected port
        1 = interrupt is fired when the pin matches the default value, 0 =
        the interrupt is fired on state change
        """

        if port == 0:
            self._bus.write_byte_data(self.__ioaddress, self.INTCONA, value)
        else:
            self._bus.write_byte_data(self.__ioaddress, self.INTCONB, value)
        return

    def set_interrupt_defaults(self, port, value):
        """
        These bits set the compare value for pins configured for
        interrupt-on-change on the selected port.
        If the associated pin level is the opposite from the register bit, an
        interrupt occurs.
        """

        if port == 0:
            self._bus.write_byte_data(self.__ioaddress, self.DEFVALA, value)
        else:
            self._bus.write_byte_data(self.__ioaddress, self.DEFVALB, value)
        return

    def set_interrupt_on_port(self, port, value):
        """
        Enable interrupts for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        value = number between 0 and 255 or 0x00 and 0xFF
        """

        if port == 0:
            self._bus.write_byte_data(self.__ioaddress, self.GPINTENA, value)
            self.__intA = value
        else:
            self._bus.write_byte_data(self.__ioaddress, self.GPINTENB, value)
            self.__intB = value
        return

    def set_interrupt_on_pin(self, pin, value):
        """
        Enable interrupts for the selected pin
        Pin = 1 to 16
        Value 0 = interrupt disabled, 1 = interrupt enabled
        """

        pin = pin - 1
        if pin < 8:
            self.__intA = self.__updatebyte(self.__intA, pin, value)
            self._bus.write_byte_data(self.__ioaddress, self.GPINTENA, self.__intA)
        else:
            self.__intB = self.__updatebyte(self.__intB, pin - 8, value)
            self._bus.write_byte_data(self.__ioaddress, self.GPINTENB, self.__intB)
        return

    def read_interrupt_status(self, port):
        """
        read the interrupt status for the pins on the selected port
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """

        if port == 0:
            return self._bus.read_byte_data(self.__ioaddress, self.INTFA)
        else:
            return self._bus.read_byte_data(self.__ioaddress, self.INTFB)

    def read_interrupt_capture(self, port):
        """
        read the value from the selected port at the time of the last
        interrupt trigger
        port 0 = pins 1 to 8, port 1 = pins 9 to 16
        """

        if port == 0:
            return self._bus.read_byte_data(self.__ioaddress, self.INTCAPA)
        else:
            return self._bus.read_byte_data(self.__ioaddress, self.INTCAPB)

    def reset_interrupts(self):
        """
        Reset the interrupts A and B to 0
        """

        self.read_interrupt_capture(0)
        self.read_interrupt_capture(1)
        return


class RTC:

    """
    Based on the Maxim DS1307

    Define registers values from datasheet
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

    # local methods

    def __init__(self, bus):
        self._bus = bus
        self.__config = self.__rtcconfig
        self._bus.write_byte_data(self.__rtcaddress, self.CONTROL, self.__config)
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
            self.__rtcaddress,
            self.SECONDS,
            self.__dec_to_bcd(
                d.second))
        self._bus.write_byte_data(
            self.__rtcaddress,
            self.MINUTES,
            self.__dec_to_bcd(
                d.minute))
        self._bus.write_byte_data(
            self.__rtcaddress,
            self.HOURS,
            self.__dec_to_bcd(
                d.hour))
        self._bus.write_byte_data(
            self.__rtcaddress,
            self.DAYOFWEEK,
            self.__dec_to_bcd(
                d.weekday()))
        self._bus.write_byte_data(
            self.__rtcaddress,
            self.DAY,
            self.__dec_to_bcd(
                d.day))
        self._bus.write_byte_data(
            self.__rtcaddress,
            self.MONTH,
            self.__dec_to_bcd(
                d.month))
        self._bus.write_byte_data(
            self.__rtcaddress,
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

        seconds, minutes, hours, dayofweek, day, month, year \
            =self._bus.read_i2c_block_data(self.__rtcaddress, 0, 7)
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
        self._bus.write_byte_data(self.__rtcaddress, self.CONTROL, self.__config)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__config = self.__updatebyte(self.__config, 7, 0)
        self.__config = self.__updatebyte(self.__config, 4, 0)
        self._bus.write_byte_data(self.__rtcaddress, self.CONTROL, self.__config)
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
        self._bus.write_byte_data(self.__rtcaddress, self.CONTROL, self.__config)
        return
