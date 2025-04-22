#!/usr/bin/env python

"""
================================================
ADCPi Python Library
================================================

Library for the ADC Differential Pi and Delta-Sigma Pi expansion boards from AB Electronics UK
for the Raspberry Pi and other compatible single-board computers.

https://www.abelectronics.co.uk/p/65/adc-differential-pi

Designed for use with the Microchip MCP3424 Delta-Sigma ADC.

This library provides functions for reading analogue voltages across 8 channels
with 12, 14, 16, or 18-bit resolutions.

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
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
try:
    from smbus2 import SMBus
except ImportError:
    try:
        from smbus import SMBus
    except ImportError:
        raise ImportError("python-smbus or smbus2 not found")
import re
import platform
import time


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ADCTimeoutError(Error):
    """The ADC operation exceeded the given deadline."""

    def __init__(self, message, timeout=None, operation=None):
        self.timeout = timeout
        self.operation = operation
        super().__init__(message)


class ADCDifferentialPi(object):
    """
    Control the MCP3424 ADC on the ADC Differential Pi and Delta-Sigma Pi
    """
    # internal variables
    __adc1_address = 0x68
    __adc2_address = 0x69

    __adc1_conf = 0x9C
    __adc2_conf = 0x9C

    __adc1_channel = 0x01
    __adc2_channel = 0x01

    __bit_mode = 18  # current bit mode
    __conversion_mode = 1  # Conversion Mode
    __pga = float(1)  # current PGA setting
    __lsb = float(0.000015625)  # default LSB value for 18 bit
    __signbit = 0  # stores the sign bit for the sampled value

    # create a byte array and fill it with initial values to define the size
    __adc_reading = bytearray([0, 0, 0, 0])

    __bus = None

    # local methods

    @staticmethod
    def __detect_raspberry_pi_bus():
        """
        Detect the appropriate I2C bus for Raspberry Pi models

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
            }

            # Get device name
            device = platform.uname()[1]

            # Get the bus number from the map or detect for Raspberry Pi
            if device in device_bus_map:
                i2c_bus = device_bus_map[device]
            elif device == "raspberrypi":
                i2c_bus = ADCDifferentialPi.__detect_raspberry_pi_bus()
            else:
                i2c_bus = 1  # Default to bus 1 for unknown devices

        try:
            return SMBus(i2c_bus)
        except FileNotFoundError:
            raise FileNotFoundError("Bus not found. Check that you have selected the correct I2C bus.")
        except IOError as err:
            raise IOError(f"I/O error: {err}")

    @staticmethod
    def __update_byte(byte, mask, value):
        """
        Internal method for setting the value of a single bit within a byte

        :param byte: input value
        :type byte: int
        :param mask: location to update
        :type mask: int
        :param value: new bit, 0 or 1
        :type value: int
        :return: updated value
        :rtype: int
        """
        byte &= mask
        byte |= value
        return byte

    def __set_channel(self, channel):
        """
        Internal method for updating the config to the selected channel

        :param channel: selected channel
        :type channel: int
        """
        if channel < 5:
            if channel != self.__adc1_channel:
                self.__adc1_channel = channel
                if channel == 1:  # bit 5 = 0, bit 6 = 0
                    self.__adc1_conf = self.__update_byte(self.__adc1_conf,
                                                          0x9F, 0x00)
                elif channel == 2:  # bit 5 = 1, bit 6 = 0
                    self.__adc1_conf = self.__update_byte(self.__adc1_conf,
                                                          0x9F, 0x20)
                elif channel == 3:  # bit 5 = 0, bit 6 = 1
                    self.__adc1_conf = self.__update_byte(self.__adc1_conf,
                                                          0x9F, 0x40)
                elif channel == 4:  # bit 5 = 1, bit 6 = 1
                    self.__adc1_conf = self.__update_byte(self.__adc1_conf,
                                                          0x9F, 0x60)
        else:
            if channel != self.__adc2_channel:
                self.__adc2_channel = channel
                if channel == 5:  # bit 5 = 0, bit 6 = 0
                    self.__adc2_conf = self.__update_byte(self.__adc2_conf,
                                                          0x9F, 0x00)
                elif channel == 6:  # bit 5 = 1, bit 6 = 0
                    self.__adc2_conf = self.__update_byte(self.__adc2_conf,
                                                          0x9F, 0x20)
                elif channel == 7:  # bit 5 = 0, bit 6 = 1
                    self.__adc2_conf = self.__update_byte(self.__adc2_conf,
                                                          0x9F, 0x40)
                elif channel == 8:  # bit 5 = 1, bit 6 = 1
                    self.__adc2_conf = self.__update_byte(self.__adc2_conf,
                                                          0x9F, 0x60)
        return

    # init object with i2c address, default is 0x68, 0x69 for ADCoPi board
    def __init__(self, address=0x68, address2=0x69, mode=18, bus=None):
        """
        Class constructor - Initialise the two ADC chips with their
        I2C addresses and bit mode.

        :param address: I2C address for channels 1 to 4, defaults to 0x68
        :type address: int, optional
        :param address2: I2C address for channels 5 to 8, defaults to 0x69
        :type address2: int, optional
        :param mode: bit mode, defaults to 18
        :type mode: int, optional
        :param bus: I2C bus number.  If no value is set, the class will try to
                    find the i2c bus automatically using the device name
        :type bus: int, optional
        """

        self.__bus = self.__get_smbus(bus)
        if 0x68 <= address <= 0x6F:
            self.__adc1_address = address
        else:
            raise ValueError('address out of range 0x68 to 0x6F')

        if 0x68 <= address2 <= 0x6F:
            self.__adc2_address = address2
        else:
            raise ValueError('address2 out of range 0x68 to 0x6F')
        self.set_bit_mode(mode)

    def set_i2c_address1(self, address):
        """
        Set the I2C address for the ADC on channels 1 to 4

        :param address: I2C address for channels 1 to 4, defaults to 0x68
        :type address: int, optional
        :raises ValueError: address out of range 0x68 to 0x6F
        """
        if 0x68 <= address <= 0x6F:
            self.__adc1_address = address
        else:
            raise ValueError('address out of range 0x68 to 0x6F')

    def set_i2caddress2(self, address):
        """
        Set the I2C address for the ADC on channels 5 to 8

        :param address: I2C address for channels 5 to 8, defaults to 0x68
        :type address: int, optional
        :raises ValueError: address out of range 0x68 to 0x6F
        """
        if 0x68 <= address <= 0x6F:
            self.__adc2_address = address
        else:
            raise ValueError('address out of range 0x68 to 0x6F')

    def get_i2c_address1(self):
        """
        Get the I2C address for the ADC on channels 1 to 4
        :return: I2C address
        :rtype: number
        """
        return self.__adc1_address

    def get_i2c_address2(self):
        """
        Get the I2C address for the ADC on channels 5 to 8
        :return: I2C address
        :rtype: number
        """
        return self.__adc2_address

    def read_voltage(self, channel: int) -> float:
        """
        Reads the voltage from the specified channel of a connected device.

        This method retrieves the raw data from the given channel and computes the
        voltage value based on the device's configuration, including the programmable gain amplifier (PGA).

        The method ensures the channel number is within the valid range to
        avoid miscommunication or invalid data readings.

        Parameters:
            channel (int): The channel number to read from. Must be in the range [1, 8].

        Raises:
            ValueError: If the channel is not within the valid range [1, 8].

        Returns:
            float: The computed voltage value for the specified channel.
        """
        if channel < 1 or channel > 8:
            raise ValueError('read_voltage: channel out of range (1 to 8 allowed)')

        raw = self.read_raw(channel)

        voltage = raw * (self.__lsb / self.__pga)

        return float(voltage)

    def read_raw(self, channel: int) -> int:
        """
        Reads the raw digital value from the specified ADC channel after ensuring proper
        configuration and handling ADC bit resolution, conversion timing, and potential
        errors during the process.

        Parameters:
            channel (int): The ADC channel to be read. Must be within the range 1 to 8.

        Returns:
            int: The raw digital value read from the specified ADC channel.

        Raises:
            ValueError: If the provided channel is out of the allowable range (1 to 8).
            ADCTimeoutError: If the ADC conversion times out before producing a result.
        """
        if channel < 1 or channel > 8:
            raise ValueError('read_raw: channel out of range (1 to 8 allowed)')

        low = 0

        # get the config and i2c address for the selected channel
        self.__set_channel(channel)
        if channel <= 4:
            config = self.__adc1_conf
            address = self.__adc1_address
        else:
            config = self.__adc2_conf
            address = self.__adc2_address

        # if the conversion mode is set to one-shot, update the ready bit to 1
        if self.__conversion_mode == 0:
            config = config | (1 << 7)
            self.__bus.write_byte(address, config)
            config = config & ~(1 << 7)  # reset the ready bit to 0

        # determine a reasonable amount of time to wait for the conversion
        seconds_per_sample = 0.26666  # default for 18 bits

        if self.__bit_mode == 16:
            seconds_per_sample = 0.06666
        elif self.__bit_mode == 14:
            seconds_per_sample = 0.01666
        elif self.__bit_mode == 12:
            seconds_per_sample = 0.00416
        timeout_time = time.monotonic() + (100 * seconds_per_sample)

        # keep reading the ADC data until the conversion result is ready
        while True:
            __adc_reading = self.__bus.read_i2c_block_data(address, config, 4)
            if self.__bit_mode == 18:
                high = __adc_reading[0]
                mid = __adc_reading[1]
                low = __adc_reading[2]
                cmd_byte = __adc_reading[3]
            else:
                high = __adc_reading[0]
                mid = __adc_reading[1]
                cmd_byte = __adc_reading[2]
            # check if bit 7 of the command byte is 0.
            if (cmd_byte & (1 << 7)) == 0:
                break
            elif time.monotonic() > timeout_time:
                msg = 'read_raw: channel %i conversion timed out' % channel
                raise ADCTimeoutError(msg)
            else:
                time.sleep(0.00001)  # sleep for 10 microseconds

        self.__signbit = False
        raw = 0
        # extract the returned bytes and combine them in the correct order
        if self.__bit_mode == 18:
            raw = ((high & 0x03) << 16) | (mid << 8) | low
            self.__signbit = bool(raw & (1 << 17))
            if raw <= 131071:
                raw = raw
            else:
                raw = raw - 262144

        elif self.__bit_mode == 16:
            raw = (high << 8) | mid
            self.__signbit = bool(raw & (1 << 15))
            if raw <= 32767:
                raw = raw
            else:
                raw = raw - 65536

        elif self.__bit_mode == 14:
            raw = ((high & 0b00111111) << 8) | mid
            self.__signbit = bool(raw & (1 << 13))
            if raw <= 8191:
                raw = raw
            else:
                raw = raw - 16384

        elif self.__bit_mode == 12:
            raw = ((high & 0x0f) << 8) | mid
            self.__signbit = bool(raw & (1 << 11))
            if raw <= 2047:
                raw = raw
            else:
                raw = raw - 4096

        return raw

    def set_pga(self, gain: int):
        """
        Set PGA (programmable gain amplifier) gain selection

        :param gain: 1 = 1x, 2 = 2x, 4 = 4x, 8 = 8x
        :type gain: int
        :raises ValueError: When gain is not one of the allowed values (1, 2, 4, or 8)
        :return: None
        """
        # Define mapping of gain values to configuration bits and PGA values
        gain_config = {
            1: {"bits": 0x00, "pga_value": 1.0},
            2: {"bits": 0x01, "pga_value": 2.0},
            4: {"bits": 0x02, "pga_value": 4.0},
            8: {"bits": 0x03, "pga_value": 8.0}
        }

        # Check if the gain is valid
        if gain not in gain_config:
            raise ValueError('set_pga: gain out of range')

        # Get configuration bits and PGA value for the requested gain
        config_bits = gain_config[gain]["bits"]
        self.__pga = gain_config[gain]["pga_value"]

        # Update configuration registers for both ADCs
        self.__adc1_conf = self.__update_byte(self.__adc1_conf, 0xFC, config_bits)
        self.__adc2_conf = self.__update_byte(self.__adc2_conf, 0xFC, config_bits)

        # Write updated configurations to the ADCs
        self.__bus.write_byte(self.__adc1_address, self.__adc1_conf)
        self.__bus.write_byte(self.__adc2_address, self.__adc2_conf)


    def set_bit_rate(self, rate: int):
        """
        redirects to set_bit_mode - kept for backwards compatibility width code using set_bit_rate
        """
        self.set_bit_mode(rate)

    def set_bit_mode(self, mode: int):
        """
        Set the sample rate and resolution
        :param mode: 12 = 12 bit (240SPS max)
                     14 = 14 bit (60SPS max)
                     16 = 16 bit (15SPS max)
                     18 = 18 bit (3.75SPS max)
        :type mode: int
        :raises ValueError: set_bit_mode: mode out of range
        """
        # Configuration mask for the bit mode (bits 2 and 3)
        bit_mode_mask = 0xF3

        # Dictionary mapping bit modes to their configuration values and LSB values
        mode_config = {
            12: {"config_bits": 0x00, "lsb": 0.001},  # bit 2 = 0, bit 3 = 0
            14: {"config_bits": 0x04, "lsb": 0.00025},  # bit 2 = 1, bit 3 = 0
            16: {"config_bits": 0x08, "lsb": 0.0000625},  # bit 2 = 0, bit 3 = 1
            18: {"config_bits": 0x0C, "lsb": 0.000015625}  # bit 2 = 1, bit 3 = 1
        }

        if mode not in mode_config:
            raise ValueError('set_bit_mode: mode out of range')

        config = mode_config[mode]
        self.__adc1_conf = self.__update_byte(self.__adc1_conf, bit_mode_mask, config["config_bits"])
        self.__adc2_conf = self.__update_byte(self.__adc2_conf, bit_mode_mask, config["config_bits"])
        self.__bit_mode = mode
        self.__lsb = config["lsb"]

        # Update both ADCs with the new configuration
        self.__bus.write_byte(self.__adc1_address, self.__adc1_conf)
        self.__bus.write_byte(self.__adc2_address, self.__adc2_conf)

    def set_conversion_mode(self, mode: int):
        """
        Set the conversion mode for ADC

        :param mode: 0 = One shot conversion mode
                     1 = Continuous conversion mode
        :type mode: int
        :raises ValueError: If mode is not 0 or 1
        """
        # Define constants for clarity
        one_shot_mode = 0
        continuous_mode = 1
        conversion_bit_mask = 0xEF  # Bit 4 mask
        continuous_mode_bit = 0x10  # Bit 4 = 1

        if mode == one_shot_mode:
            # Set bit 4 to 0 for one-shot mode
            self.__adc1_conf = self.__update_byte(self.__adc1_conf, conversion_bit_mask, 0x00)
            self.__adc2_conf = self.__update_byte(self.__adc2_conf, conversion_bit_mask, 0x00)
            self.__conversion_mode = one_shot_mode
        elif mode == continuous_mode:
            # Set bit 4 to 1 for continuous mode
            self.__adc1_conf = self.__update_byte(self.__adc1_conf, conversion_bit_mask, continuous_mode_bit)
            self.__adc2_conf = self.__update_byte(self.__adc2_conf, conversion_bit_mask, continuous_mode_bit)
            self.__conversion_mode = continuous_mode
        else:
            raise ValueError('set_conversion_mode: mode out of range')

        # Write the updated configuration to both ADCs
        self.__bus.write_byte(self.__adc1_address, self.__adc1_conf)
        self.__bus.write_byte(self.__adc2_address, self.__adc2_conf)
