#!/usr/bin/python

import time
import math
import re
import RPi.GPIO as GPIO

"""
================================================
ABElectronics ServoPi 16-Channel PWM Servo Driver
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Requires python smbus to be installed
================================================
"""


class PWM:
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

    global _bus

    def __init__(self, bus, address=0x40):
        """
        init object with i2c address, default is 0x40 for ServoPi board
        """

        self.address = address
        self._bus = bus
        self.write(self.address, self.MODE1, 0x00)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)

    def set_pwm_freq(self, freq):
        """
        Set the PWM frequency
        """

        scaleval = 25000000.0    # 25MHz
        scaleval /= 4096.0       # 12-bit
        scaleval /= float(freq)
        scaleval -= 1.0
        prescale = math.floor(scaleval + 0.5)
        oldmode = self.read(self.address, self.MODE1)
        newmode = (oldmode & 0x7F) | 0x10
        self.write(self.address, self.MODE1, newmode)
        self.write(self.address, self.PRE_SCALE, int(math.floor(prescale)))
        self.write(self.address, self.MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.address, self.MODE1, oldmode | 0x80)

    def set_pwm(self, channel, on, off):
        """
        set the output on a single channel
        """

        self.write(self.address, self.LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.address, self.LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.address, self.LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.address, self.LED0_OFF_H + 4 * channel, off >> 8)

    def set_all_pwm(self, on, off):
        """
        set the output on all channels
        """

        self.write(self.address, self.ALL_LED_ON_L, on & 0xFF)
        self.write(self.address, self.ALL_LED_ON_H, on >> 8)
        self.write(self.address, self.ALL_LED_OFF_L, off & 0xFF)
        self.write(self.address, self.ALL_LED_OFF_H, off >> 8)

    def output_disable(self):
        """
        disable output via OE pin
        """

        GPIO.output(7, True)

    def output_enable(self):
        """
        enable output via OE pin
        """

        GPIO.output(7, False)
        
    def set_allcall_address(self, i2caddress):
        """
        Set the I2C address for the All Call function
        """
        oldmode = self.read(self.address, self.MODE1)
        newmode = oldmode | (1 << 0)
        self.write(self.address, self.MODE1, newmode)
        self.write(self.address, self.ALLCALLADR, i2caddress << 1)
        
    def enable_allcall_address(self):
        """
        Enable the I2C address for the All Call function
        """
        oldmode = self.read(self.address, self.MODE1)
        newmode = oldmode | (1 << 0)
        self.write(self.address, self.MODE1, newmode)
        
    def disable_allcall_address(self):
        """
        Disable the I2C address for the All Call function
        """
        oldmode = self.read(self.address, self.MODE1)
        newmode = oldmode  & ~(1 << 0)
        self.write(self.address, self.MODE1, newmode)


    def write(self, address, reg, value):
        """
        Write data to I2C bus
        """
    
        try:
            self._bus.write_byte_data(address, reg, value)
        except IOError as err:
            return err
    
    
    def read(self, address, reg):
        """
        Read data from I2C bus
        """
    
        try:
            result = self._bus.read_byte_data(address, reg)
            return result
        except IOError as err:
            return err
