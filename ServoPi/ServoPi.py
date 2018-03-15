#!/usr/bin/env python
"""
================================================
ABElectronics ServoPi 16-Channel PWM Servo Driver

Requires python smbus to be installed
================================================
"""

try:
    import smbus
except ImportError:
    raise ImportError("python-smbus not found")
import re
import time
import math
import platform
import RPi.GPIO as GPIO


class PWM(object):
    """
    PWM class for controlling the PCA9685 PWM IC
    """

    # Define registers values from datasheet
    MODE1 = 0x00
    MODE2 = 0x01
    SUBADR1 = 0x02
    SUBADR2 = 0x03
    SUBADR3 = 0x04
    ALLCALLADR = 0x05
    LED0_ON_L = 0x06
    LED0_ON_H = 0x07
    LED0_OFF_L = 0x08
    LED0_OFF_H = 0x09
    ALL_LED_ON_L = 0xFA
    ALL_LED_ON_H = 0xFB
    ALL_LED_OFF_L = 0xFC
    ALL_LED_OFF_H = 0xFD
    PRE_SCALE = 0xFE

    __address = 0x40
    __bus = None

    # local methods
    @staticmethod
    def __get_smbus():
        """
        internal method for getting an instance of the i2c bus
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
                model = re.match('(.*?)\\s*\\s*(.*)', line)
                if model:
                    (name, value) = (model.group(1), model.group(2))
                    if name == "Revision":
                        if value[-4:] in ('0002', '0003'):
                            i2c__bus = 0
                        else:
                            i2c__bus = 1
                        break
        try:
            return smbus.SMBus(i2c__bus)
        except IOError:
            raise 'Could not open the i2c bus'

    # public methods

    def __init__(self, address=0x40):
        """
        init object with i2c address, default is 0x40 for ServoPi board
        """

        self.__address = address
        self.__bus = self.__get_smbus()
        self.__write(self.MODE1, 0x00)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)

    def set_pwm_freq(self, freq):
        """
        Set the PWM frequency - 40 to 1000
        """
        if freq < 40 or freq > 1000:
            raise ValueError('set_pwm_freq: freq out of range')

        scaleval = 25000000.0    # 25MHz
        scaleval /= 4096.0       # 12-bit
        scaleval /= float(freq)
        scaleval -= 1.0
        prescale = math.floor(scaleval + 0.5)
        oldmode = self.__read(self.MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.__write(self.MODE1, newmode)
        self.__write(self.PRE_SCALE, int(math.floor(prescale)))
        self.__write(self.MODE1, oldmode)
        time.sleep(0.005)
        self.__write(self.MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on_time, off_time):
        """
        set the output on a single channel
        """

        if channel < 1 or channel > 16:
            raise ValueError('set_pwm: channel out of range')

        if on_time < 0 or on_time > 4095:
            raise ValueError('set_pwm: on_time out of range')

        if off_time < 0 or off_time > 4095:
            raise ValueError('set_pwm: off_time out of range')

        if (on_time + off_time) > 4095:
            raise ValueError('set_pwm: on_time + off_time greater than 4095')

        channel = channel - 1

        self.__write(self.LED0_ON_L + 4 * channel,
                     on_time & 0xFF)
        self.__write(self.LED0_ON_H + 4 * channel, on_time >> 8)
        self.__write(self.LED0_OFF_L + 4 * channel,
                     off_time & 0xFF)
        self.__write(self.LED0_OFF_H + 4 * channel,
                     off_time >> 8)

    def set_all_pwm(self, on_time, off_time):
        """
        set the output on all channels
        """

        if on_time < 0 or on_time > 4095:
            raise ValueError('set_all_pwm: on_time out of range')

        if off_time < 0 or off_time > 4095:
            raise ValueError('set_all_pwm: off_time out of range')

        if (on_time + off_time) > 4095:
            raise ValueError('set_all_pwm: on_time + off_time must not \
                             exceed 4095')

        self.__write(self.ALL_LED_ON_L, on_time & 0xFF)
        self.__write(self.ALL_LED_ON_H, on_time >> 8)
        self.__write(self.ALL_LED_OFF_L, off_time & 0xFF)
        self.__write(self.ALL_LED_OFF_H, off_time >> 8)

    @classmethod
    def output_disable(cls):
        """
        disable output via OE pin
        """
        try:
            GPIO.output(7, True)
        except:
            raise IOError("Failed to write to GPIO pin")

    @classmethod
    def output_enable(cls):
        """
        enable output via OE pin
        """
        try:
            GPIO.output(7, False)
        except:
            raise IOError("Failed to write to GPIO pin")

    def set_allcall_address(self, i2caddress):
        """
        Set the I2C address for the All Call function
        """
        oldmode = self.__read(self.MODE1)
        newmode = oldmode | (1 << 0)
        self.__write(self.MODE1, newmode)
        self.__write(self.ALLCALLADR, i2caddress << 1)

    def enable_allcall_address(self):
        """
        Enable the I2C address for the All Call function
        """
        oldmode = self.__read(self.MODE1)
        newmode = oldmode | (1 << 0)
        self.__write(self.MODE1, newmode)

    def disable_allcall_address(self):
        """
        Disable the I2C address for the All Call function
        """
        oldmode = self.__read(self.MODE1)
        newmode = oldmode & ~(1 << 0)
        self.__write(self.MODE1, newmode)

    def __write(self, reg, value):
        """
        Write data to I2C bus
        """
        try:
            self.__bus.write_byte_data(self.__address, reg, value)
        except IOError as err:
            return err

    def __read(self, reg):
        """
        Read data from I2C bus
        """
        try:
            result = self.__bus.read_byte_data(self.__address, reg)
            return result
        except IOError as err:
            return err


class Servo(object):
    """
    Servo class for controlling RC servos with the Servo PWM Pi Zero
    """
    __pwm = None
    __lowpos = 0
    __highpos = 4095
    __frequency = 50
    __channel = 1

    def __init__(self, address=0x40, low_limit=1.0, high_limit=2.0):
        """
        init object with i2c address, default is 0x40 for ServoPi board
        """

        self.__pwm = PWM(address)
        self.set_frequency(50)
        self.set_low_limit(low_limit)
        self.set_high_limit(high_limit)

        print(self.__lowpos)
        print(self.__highpos)

    def move(self, channel, position, steps=250):
        """
        set the position of the servo
        """
        if channel >= 1 and channel <= 16:
            self.__channel = channel
        else:
            raise ValueError('move: channel out of range')

        if steps < 0 or steps > 4095:
            raise ValueError('move: steps out of range')

        if position >= 0 and position <= steps:
            pwm_value = (((float(self.__highpos)-float(self.__lowpos)) /
                          steps) * float(position)) + self.__lowpos
            self.__pwm.set_pwm(channel, 0, int(pwm_value))

            print(pwm_value)
        else:
            raise ValueError('move: channel out of range')

    def set_low_limit(self, low_limit):
        """
        Set the low limit in milliseconds
        """
        self.__lowpos = int(4096.0 * (low_limit / 1000.0) * self.__frequency)

        if (self.__lowpos < 0) or (self.__lowpos > 4095):
            raise ValueError('set_low_limit: value out of range')

    def set_high_limit(self, high_limit):
        """
        Set the high limit in milliseconds
        """
        self.__highpos = int(4096.0 * (high_limit / 1000.0) * self.__frequency)

        if (self.__highpos < 0) or (self.__highpos > 4095):
            raise ValueError('set_high_limit: value out of range')

    def set_frequency(self, freq):
        """
        Set the PWM frequency
        """
        self.__pwm.set_pwm_freq(freq)

    def output_disable(self):
        """
        disable output via OE pin
        """
        try:
            self.__pwm.output_disable()
        except:
            raise IOError("Failed to write to GPIO pin")

    def output_enable(self):
        """
        enable output via OE pin
        """
        try:
            self.__pwm.output_enable()
        except:
            raise IOError("Failed to write to GPIO pin")
