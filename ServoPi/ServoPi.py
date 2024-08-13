#!/usr/bin/env python
"""
================================================
AB Electronics UK ServoPi 16-Channel PWM Servo Driver

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
import math
import platform
import RPi.GPIO as GPIO


class PWM(object):
    """
    PWM class for controlling the PCA9685 PWM IC
    """

    # Define registers values from the datasheet
    __MODE1 = 0x00
    __MODE2 = 0x01
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __ALLCALLADR = 0x05
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALL_LED_ON_L = 0xFA
    __ALL_LED_ON_H = 0xFB
    __ALL_LED_OFF_L = 0xFC
    __ALL_LED_OFF_H = 0xFD
    __PRE_SCALE = 0xFE

    # Define mode bits
    __MODE1_EXTCLK = 6  # use external clock
    __MODE1_SLEEP = 4  # sleep mode
    __MODE1_ALLCALL = 0  # all call address

    __MODE2_INVRT = 4  # invert output
    __MODE2_OCH = 3  # output type
    __MODE2_OUTDRV = 2  # output type
    __MODE2_OUTNE1 = 0  # output mode when not enabled

    # Local variables
    __mode1_default = 0x00
    __mode2_default = 0x0C
    __oe_pin = 7
    __address = 0x40
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
        i2c__bus = 1
        if bus is not None:
            i2c__bus = bus
        else:
            # detect the device that is being used
            device = platform.uname()[1]

            if device == "orangepione":  # orange pi one
                i2c__bus = 0

            elif device == "orangepizero2":  # orange pi zero 2
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
                # detect I2C port number and assign to i2c__bus
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

    def __write(self, reg, value):
        """
        Internal method for writing data to the I2C bus

        :param value: value to write
        :type value: int
        :return: IOError
        :rtype: IOError
        """
        try:
            self.__bus.write_byte_data(self.__address, reg, value)
        except IOError as err:
            return err

    def __read(self, reg):
        """
        Internal method for reading data from the I2C bus

        :return: IOError
        :rtype: IOError
        """
        try:
            result = self.__bus.read_byte_data(self.__address, reg)
            return result
        except IOError as err:
            return err

    # public methods

    def __init__(self, address=0x40, bus=None):
        """
        init object with I2C address, default is 0x40 for ServoPi board

        :param address: device I2C address, defaults to 0x40
        :type address: int, optional
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the I2C bus automatically using the device name
        :type bus: int, optional
        """
        self.__address = address
        self.__bus = self.__get_smbus(bus)
        self.__write(self.__MODE1, self.__mode1_default)
        self.__write(self.__MODE2, self.__mode2_default)
        GPIO.setwarnings(False)

        mode = GPIO.getmode()  # Check if the GPIO mode has been set

        if mode == 10:  # Mode set to GPIO.BOARD
            self.__oe_pin = 7
        elif mode == 11:  # Mode set to GPIO.BCM
            self.__oe_pin = 4
        else:  # Mode not set
            GPIO.setmode(GPIO.BOARD)
            self.__oe_pin = 7

        GPIO.setup(self.__oe_pin, GPIO.OUT)

    def set_pwm_freq(self, freq, calibration=0):
        """
        Set the PWM frequency

        :param freq: 40 to 1000
        :type freq: int
        :param calibration: optional integer value to offset oscillator errors.
                            defaults to 0
        :type calibration: int, optional
        :raises ValueError: set_pwm_freq: freq out of range
        """
        if freq < 40 or freq > 1000:
            raise ValueError('set_pwm_freq: freq out of range')

        scale_value = 25000000.0    # 25MHz
        scale_value /= 4096.0       # 12-bit
        scale_value /= float(freq)
        scale_value -= 1.0
        pre_scaler = math.floor(scale_value + 0.5)
        pre_scaler = pre_scaler + calibration
        old_mode = self.__read(self.__MODE1)
        new_mode = (old_mode & 0x7F) | 0x10
        self.__write(self.__MODE1, new_mode)
        self.__write(self.__PRE_SCALE, int(pre_scaler))
        self.__write(self.__MODE1, old_mode)
        time.sleep(0.005)
        self.__write(self.__MODE1, old_mode | 0x80)

    def set_pwm(self, channel, on_time, off_time):
        """
        Set the output on a single channel

        :param channel: 1 to 16
        :type channel: int
        :param on_time: 0 to 4095
        :type on_time: int
        :param off_time: 0 to 4095
        :type off_time: int
        :raises ValueError: set_pwm: channel out of range
        :raises ValueError: set_pwm: on_time out of range
        :raises ValueError: set_pwm: off_time out of range
        :raises ValueError: set_pwm: on_time greater than off_time
        """

        if channel < 1 or channel > 16:
            raise ValueError('set_pwm: channel out of range')

        if on_time < 0 or on_time > 4095:
            raise ValueError('set_pwm: on_time out of range')

        if off_time < 0 or off_time > 4095:
            raise ValueError('set_pwm: off_time out of range')

        if on_time > off_time:
            raise ValueError('set_pwm: on_time greater than off_time')

        channel = channel - 1

        self.__write(self.__LED0_ON_L + 4 * channel,
                     on_time & 0xFF)
        self.__write(self.__LED0_ON_H + 4 * channel, on_time >> 8)
        self.__write(self.__LED0_OFF_L + 4 * channel,
                     off_time & 0xFF)
        self.__write(self.__LED0_OFF_H + 4 * channel,
                     off_time >> 8)

    def set_pwm_on_time(self, channel, on_time):
        """
        Set the output on time on a single channel

        :param channel: 1 to 16
        :type channel: int
        :param on_time: 0 to 4095
        :type on_time: int
        :raises ValueError: set_pwm_on_time: channel out of range
        :raises ValueError: set_pwm_on_time: on_time out of range
        """
        if channel < 1 or channel > 16:
            raise ValueError('set_pwm_on_time: channel out of range')

        if on_time < 0 or on_time > 4095:
            raise ValueError('set_pwm_on_time: on_time out of range')

        channel = channel - 1

        self.__write(self.__LED0_ON_L + 4 * channel,
                     on_time & 0xFF)
        self.__write(self.__LED0_ON_H + 4 * channel, on_time >> 8)

    def set_pwm_off_time(self, channel, off_time):
        """
        Set the output off time on a single channel

        :param channel: 1 to 16
        :type channel: int
        :param off_time: 0 to 4095
        :type off_time: int
        :raises ValueError: set_pwm_off_time: channel out of range
        :raises ValueError: set_pwm_off_time: off_time out of range
        """
        if channel < 1 or channel > 16:
            raise ValueError('set_pwm_off_time: channel out of range')

        if off_time < 0 or off_time > 4095:
            raise ValueError('set_pwm_off_time: off_time out of range')

        channel = channel - 1

        self.__write(self.__LED0_OFF_L + 4 * channel,
                     off_time & 0xFF)
        self.__write(self.__LED0_OFF_H + 4 * channel,
                     off_time >> 8)

    def get_pwm_on_time(self, channel):
        """
        Get the on time for the selected channel

        :param channel: 1 to 16
        :type channel: int
        :raises ValueError: get_pwm_on_time: channel out of range
        :return: 0 to 4095
        :rtype: int
        """
        if channel < 1 or channel > 16:
            raise ValueError('get_pwm_on_time: channel out of range')

        channel = channel - 1
        low_byte = self.__read(self.__LED0_ON_L + 4 * channel)
        high_byte = self.__read(self.__LED0_ON_H + 4 * channel)
        value = low_byte | high_byte << 8

        return value

    def get_pwm_off_time(self, channel):
        """
        Get the on time for the selected channel

        :param channel: 1 to 16
        :type channel: int
        :raises ValueError: get_pwm_off_time: channel out of range
        :return: 0 to 4095
        :rtype: int
        """
        if channel < 1 or channel > 16:
            raise ValueError('get_pwm_off_time: channel out of range')

        channel = channel - 1
        low_byte = self.__read(self.__LED0_OFF_L + 4 * channel)
        high_byte = self.__read(self.__LED0_OFF_H + 4 * channel)
        value = low_byte | high_byte << 8

        return value

    def set_all_pwm(self, on_time, off_time):
        """
        Set the output on all channels

        :param on_time: 0 to 4095
        :type on_time: int
        :param off_time: 0 to 4095
        :type off_time: int
        :raises ValueError: set_all_pwm: on_time out of range
        :raises ValueError: set_all_pwm: off_time out of range
        :raises ValueError: set_all_pwm: on_time + off_time
                            must not exceed 4095
        """
        if on_time < 0 or on_time > 4095:
            raise ValueError('set_all_pwm: on_time out of range')

        if off_time < 0 or off_time > 4095:
            raise ValueError('set_all_pwm: off_time out of range')

        if (on_time + off_time) > 4095:
            raise ValueError('set_all_pwm: on_time + off_time must not \
                             exceed 4095')

        self.__write(self.__ALL_LED_ON_L, on_time & 0xFF)
        self.__write(self.__ALL_LED_ON_H, on_time >> 8)
        self.__write(self.__ALL_LED_OFF_L, off_time & 0xFF)
        self.__write(self.__ALL_LED_OFF_H, off_time >> 8)

    def output_disable(self):
        """
        Disable output via OE pin

        :raises IOError: Failed to write to GPIO pin
        """
        try:
            GPIO.output(self.__oe_pin, True)
        except IOError:
            raise IOError("Failed to write to GPIO pin")

    def output_enable(self):
        """
        Enable output via OE pin

        :raises IOError: Failed to write to GPIO pin
        """
        try:
            GPIO.output(self.__oe_pin, False)
        except IOError:
            raise IOError("Failed to write to GPIO pin")

    def set_allcall_address(self, i2caddress):
        """
        Set the I2C address for the All Call function

        :param i2caddress: I2C address for the All Call function
        :type i2caddress: int
        """
        old_mode = self.__read(self.__MODE1)
        new_mode = old_mode | (1 << self.__MODE1_ALLCALL)
        self.__write(self.__MODE1, new_mode)
        self.__write(self.__ALLCALLADR, i2caddress << 1)

    def enable_allcall_address(self):
        """
        Enable the I2C address for the All Call function
        """
        old_mode = self.__read(self.__MODE1)
        new_mode = old_mode | (1 << self.__MODE1_ALLCALL)
        self.__write(self.__MODE1, new_mode)

    def disable_allcall_address(self):
        """
        Disable the I2C address for the All Call function
        """
        old_mode = self.__read(self.__MODE1)
        new_mode = old_mode & ~(1 << self.__MODE1_ALLCALL)
        self.__write(self.__MODE1, new_mode)

    def sleep(self):
        """
        Put the device into a sleep state
        """
        old_mode = self.__read(self.__MODE1)
        new_mode = old_mode | (1 << self.__MODE1_SLEEP)
        self.__write(self.__MODE1, new_mode)

    def wake(self):
        """
        Wake the device from its sleep state
        """
        old_mode = self.__read(self.__MODE1)
        new_mode = old_mode & ~(1 << self.__MODE1_SLEEP)
        self.__write(self.__MODE1, new_mode)

    def is_sleeping(self):
        """
        Check the sleep status of the device

        :return: True or False
        :rtype: bool
        """
        register_value = self.__read(self.__MODE1)
        if self.__check_bit(register_value, self.__MODE1_SLEEP):
            return True
        else:
            return False

    def invert_output(self, state):
        """
        Invert the PWM output on all channels

        :param state: True = inverted, False = non-inverted
        :type state: bool
        """
        if state is True:
            old_mode = self.__read(self.__MODE2)
            new_mode = old_mode | (1 << self.__MODE2_INVRT)
            self.__write(self.__MODE2, new_mode)
        else:
            old_mode = self.__read(self.__MODE2)
            new_mode = old_mode & ~(1 << self.__MODE2_INVRT)
            self.__write(self.__MODE2, new_mode)


class Servo(object):
    """
    Servo class for controlling RC servos with the Servo PWM Pi Zero
    """
    __pwm = None
    __position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __low_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __high_position = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __use_offset = False
    __offset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    __frequency = 50

    # local methods

    def __refresh_channels(self):
        """
        Internal method for refreshing the servo positions
        """
        for i in range(0, 16):
            if self.__position == 0:
                self.__pwm.set_pwm(i+1, 0, 0)
            else:
                if self.__use_offset is True:
                    self.__pwm.set_pwm(i+1, self.__offset[i],
                                       self.__position[i] + self.__offset[i])
                else:
                    self.__pwm.set_pwm(i+1, 0, self.__position[i])

    def __calculate_offsets(self):
        """
        Internal method for calculating the start positions
        to stagger the servo position pulses
        """
        x = 0
        for i in range(0, 16):
            x = x + self.__high_position[i]
            if x > 4095 - self.__high_position[i]:
                x = self.__high_position[0] / 2
            self.__offset[i] = x
        self.__refresh_channels()

    # public methods

    def __init__(self, address=0x40, low_limit=1.0,
                 high_limit=2.0, reset=True, bus=None):
        """
        Initialise the Servo object

        :param address: i2c address for the ServoPi board, defaults to 0x40
        :type address: int, optional
        :param low_limit: Pulse length in milliseconds for the
                          lower servo limit; defaults to 1.0
        :type low_limit: float, optional
        :param high_limit: Pulse length in milliseconds for the
                           upper servo limit; defaults to 2.0
        :type high_limit: float, optional
        :param reset: True = reset the controller and turn off all channels.
                      False = keep existing servo positions and frequency.
                      defaults to True
        :type reset: bool, optional
        :param bus: I2C bus number.  If no value is set the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int, optional
        """

        self.__pwm = PWM(address, bus)
        self.set_low_limit(low_limit)
        self.set_high_limit(high_limit)

        if reset is True:
            self.set_frequency(50)
            self.__calculate_offsets()  # reset the offset values
        else:
            # get the on and off times from the pwm controller
            for i in range(0, 16):
                self.__offset[i] = self.__pwm.get_pwm_on_time(i + 1)
                self.__position[i] = self.__pwm.get_pwm_off_time(i + 1) - self.__offset[i]

    def move(self, channel, position, steps=250):
        """
        Set the servo position

        :param channel: 1 to 16
        :type channel: int
        :param position:  value between 0 and the maximum number of steps.
        :type position: int
        :param steps: The number of steps between the low and high limits.
                      This can be any number between 0 and 4095.
                      On a typical RC servo, a value of 250 is recommended.
                      Defaults to 250.
        :type steps: int, optional
        :raises ValueError: move: channel out of range
        :raises ValueError: move: steps out of range
        :raises ValueError: move: position out of range
        """
        if channel < 1 or channel > 16:
            raise ValueError('move: channel out of range')

        if steps < 0 or steps > 4095:
            raise ValueError('move: steps out of range')

        if 0 <= position <= steps:
            high = float(self.__high_position[channel - 1])
            low = float(self.__low_position[channel - 1])

            pwm_value = int((((high - low) / float(steps)) *
                            float(position)) + low)

            self.__position[channel - 1] = pwm_value

            if self.__use_offset:
                self.__pwm.set_pwm(channel, self.__offset[channel - 1],
                                   pwm_value + self.__offset[channel - 1])

            else:
                self.__pwm.set_pwm(channel, 0, pwm_value)
        else:
            raise ValueError('move: position out of range')

    def get_position(self, channel, steps=250):
        """
        Get the servo position

        :param channel: 1 to 16
        :type channel: int
        :param steps: The number of steps between the low and high limits.
                      This can be any number between 0 and 4095.
                      On a typical RC servo, a value of 250 is recommended.
                      Defaults to 250.
        :type steps: int, optional
        :raises ValueError: get_position: channel out of range
        :return: position - value between 0 and the maximum number of steps.
                 Due to rounding errors when calculating the position, the
                 returned value may not be the same as the set value.
        :rtype: int
        """
        if channel < 1 or channel > 16:
            raise ValueError('get_position: channel out of range')

        pwm_value = float(self.__pwm.get_pwm_off_time(channel))

        if self.__use_offset:
            pwm_value = pwm_value - self.__offset[channel - 1]

        steps = float(steps)
        high = float(self.__high_position[channel - 1])
        low = float(self.__low_position[channel - 1])

        position = int(math.ceil((steps * (pwm_value - low)) / (high - low)))

        return position

    def set_low_limit(self, low_limit, channel=0):
        """
        Set the pulse length for the lower servo limits. Typically around 1ms.
        Warning: Setting the pulse limit below 1ms may damage your servo.

        :param low_limit: Pulse length in milliseconds for the lower limit.
        :type low_limit: float
        :param channel: The channel for which the low limit will be set.
                        If this value is omitted the low limit will be
                        set for all channels., defaults to 0
        :type channel: int, optional
        :raises ValueError: set_low_limit: channel out of range
        :raises ValueError: set_low_limit: low limit out of range
        """

        if channel < 0 or channel > 16:
            raise ValueError('set_low_limit: channel out of range')

        low_position = int(4096.0 * (low_limit / 1000.0) * self.__frequency)

        if (low_position < 0) or (low_position > 4095):
            raise ValueError('set_low_limit: low limit out of range')

        if 1 <= channel <= 16:
            # update the specified channel
            self.__low_position[channel - 1] = low_position
        else:
            # no channel specified so update all channels
            for i in range(16):
                self.__low_position[i] = low_position

    def set_high_limit(self, high_limit, channel=0):
        """
        Set the pulse length for the upper servo limits. Typically around 2ms.
        Warning: Setting the pulse limit above 2ms may damage your servo.

        :param high_limit: Pulse length in milliseconds for the upper limit.
        :type high_limit: float
        :param channel: The channel for which the upper limit will be set.
                        If this value is omitted the upper limit will be
                        set for all channels., defaults to 0
        :type channel: int, optional
        :raises ValueError: set_high_limit: channel out of range
        :raises ValueError: set_high_limit: high limit out of range
        """

        if channel < 0 or channel > 16:
            raise ValueError('set_high_limit: channel out of range')

        high_position = int(4096.0 * (high_limit / 1000.0) * self.__frequency)

        if (high_position < 0) or (high_position > 4095):
            raise ValueError('set_high_limit: high limit out of range')

        if 1 <= channel <= 16:
            # update the specified channel
            self.__high_position[channel - 1] = high_position
        else:
            # no channel specified so update all channels
            for i in range(16):
                self.__high_position[i] = high_position

    def set_frequency(self, freq, calibration=0):
        """
        Set the PWM frequency

        :param freq: 40 to 1000
        :type freq: int
        :param calibration: Optional integer value to offset oscillator errors.
                            defaults to 0
        :type calibration: int, optional
        """
        self.__pwm.set_pwm_freq(freq, calibration)
        self.__frequency = freq

    def output_disable(self):
        """
        Disable output via OE pin

        :raises IOError: Failed to write to GPIO pin
        """
        try:
            self.__pwm.output_disable()
        except IOError:
            raise IOError("Failed to write to GPIO pin")

    def output_enable(self):
        """
        Enable output via OE pin

        :raises IOError: Failed to write to GPIO pin
        """
        try:
            self.__pwm.output_enable()
            self.__calculate_offsets()  # update the offset values
        except IOError:
            raise IOError("Failed to write to GPIO pin")

    def offset_enable(self):
        """
        Enable pulse offsets.
        This will set servo pulses to be staggered across the channels
        to reduce surges in the current draw
        """
        self.__use_offset = True
        self.__calculate_offsets()  # update the offset values

    def offset_disable(self):
        """
        Disable pulse offsets.
        This will set all servo pulses to start at the same time.
        """
        self.__use_offset = False
        self.__refresh_channels()  # refresh the channel locations

    def sleep(self):
        """
        Put the device into a sleep state
        """
        self.__pwm.sleep()

    def wake(self):
        """
        Wake the device from its sleep state
        """
        self.__pwm.wake()

    def is_sleeping(self):
        """
        Check the sleep status of the device
        """
        return self.__pwm.is_sleeping()
