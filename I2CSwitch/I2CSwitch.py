#!/usr/bin/env python
"""
================================================
ABElectronics I2CSwitch - 4 Channel I2C Switch

Requires smbus2 or python smbus to be installed
================================================
"""

try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
import re
import time
import types
import platform
import RPi.GPIO as GPIO


class I2CSwitch(object):
    """
    I2CSwitch class for controlling the PCA9546A I2C Switch
    """

    # define GPIO Reset Pin
    __RESETPIN = 13

    # local variables
    __ctl = 0x00
    __address = 0x70
    __bus = None

    # local methods
    @staticmethod
    def __get_smbus(bus):
        """
        Internal method for getting an instance of the i2c bus

        :param bus: I2C bus number.  If value is None the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int
        :return: i2c bus for target device
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

    def __write(self, value):
        """
        Internal method to write data to I2C bus

        :param value: value to write
        :type value: int
        :return: IOError
        :rtype: IOError
        """
        try:
            self.__bus.write_byte(self.__address, value)
        except IOError as err:
            return err

    def __read(self):
        """
        Internal method to read data from I2C bus

        :return: IOError
        :rtype: IOError
        """
        try:
            result = self.__bus.read_byte(self.__address)
            return result
        except IOError as err:
            return err

    # public methods

    def __init__(self, address=0x70, bus=None):
        """
        Initialise object with i2c address for the I2C Switch board

        :param address: device i2c address, defaults to 0x70
        :type address: int, optional
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int, optional
        """
        self.__address = address
        self.__bus = self.__get_smbus(bus)
        self.__write(self.__ctl)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__RESETPIN, GPIO.OUT)
        GPIO.output(self.__RESETPIN, True)

    def switch_channel(self, channel):
        """
        Enable the specified I2C channel and disable other channels

        :param channel: 1 to 4
        :type channel: int
        :raises ValueError: set_channel: channel out of range (1 to 4)
        """
        if channel < 1 or channel > 4:
            raise ValueError('set_channel: channel out of range (1 to 4)')
        else:
            self.__ctl = 0
            self.__ctl = self.__updatebyte(self.__ctl, channel - 1, 1)
            self.__write(self.__ctl)

    def set_channel_state(self, channel, state):
        """
        Set the state of an individual I2C channel

        :param channel: 1 to 4
        :type channel: int
        :param state: True of False
        :type state: bool
        :raises ValueError: set_channel: channel out of range (1 to 4)
        :raises ValueError: set_channel: state out of range (True or False)
        """
        if channel < 1 or channel > 4:
            raise ValueError('set_channel: channel out of range (1 to 4)')
        if type(state) != bool:
            raise ValueError('set_channel: state out of range (True or False)')
        else:
            if state is True:
                self.__ctl = self.__updatebyte(self.__ctl, channel - 1, 1)
            else:
                self.__ctl = self.__updatebyte(self.__ctl, channel - 1, 0)
            self.__write(self.__ctl)

    def get_channel_state(self, channel):
        """
        Get the state of an individual I2C channel

        :param channel: 1 to 4
        :type channel: int
        :raises ValueError: set_channel: channel out of range (1 to 4)
        :return: True = channel enabled, False = channel disabled
        :rtype: bool
        """
        if channel < 1 or channel > 4:
            raise ValueError('set_channel: channel out of range (1 to 4)')
        else:
            ctrreg = self.__read()
            if (self.__checkbit(ctrreg, channel - 1) == 1):
                return True
            else:
                return False

    def reset(self):
        """
        Reset the PCA9546A I2C switch.
        Resetting allows the PCA9546A to recover from a situation in which one
        of the downstream I2C buses is stuck in a low state.
        All channels will be set to an off state.

        :raises ValueError: Failed to write to GPIO pin
        """
        try:
            GPIO.output(self.__RESETPIN, False)
            # wait 1 millisecond before setting the pin high again
            time.sleep(0.001)
            GPIO.output(self.__RESETPIN, True)
            # wait another 1 millisecond for the device to reset
            time.sleep(0.001)
        except IOError as err:
            raise IOError("Failed to write to GPIO pin: " + err)
