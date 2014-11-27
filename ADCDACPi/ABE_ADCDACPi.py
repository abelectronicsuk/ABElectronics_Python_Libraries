#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev

"""
================================================
ABElectronics ADCDAC Pi Analogue to Digital / Digital to Analogue Converter
Version 1.0 Created 16/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
================================================

Based on the Microchip MCP3202 and MCP4822
"""


class ADCDACPi:

    # variables
    __adcrefvoltage = 3.3  # reference voltage for the ADC chip.

    # Define SPI bus and init
    spiADC = spidev.SpiDev()
    spiADC.open(0, 0)
    spiADC.max_speed_hz = (4000000)

    spiDAC = spidev.SpiDev()
    spiDAC.open(0, 1)
    spiDAC.max_speed_hz = (4000000)

    # public methods

    def read_adc_voltage(self, channel):
        """
         Read the voltage from the selected channel on the ADC
         Channel = 1 or 2
         """
        if ((channel > 2) or (channel < 1)):
            print 'ADC channel needs to be 1 or 2'
        raw = self.read_adc_raw(channel)
        voltage = (self.__adcrefvoltage / 4096) * raw
        return voltage

    def read_adc_raw(self, channel):
        # Read the raw value from the selected channel on the ADC
        # Channel = 1 or 2
        if ((channel > 2) or (channel < 1)):
            print 'ADC channel needs to be 1 or 2'
        r = self.spiADC.xfer2([1, (1 + channel) << 6, 0])
        ret = ((r[1] & 0x0F) << 8) + (r[2])
        return ret

    def set_adc_refvoltage(self, voltage):
        """
        set the reference voltage for the analogue to digital converter.
        The ADC uses the raspberry pi 3.3V power as a voltage reference so
        using this method to set the reference to match the
        exact output voltage from the 3.3V regulator will increase the
        accuracy of the ADC readings.
        """
        if (voltage >= 0.0) and (voltage <= 7.0):
            __adcrefvoltage = voltage
        else:
            print 'reference voltage out of range'
        return

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
        self.spiDAC.xfer2([highByte, lowByte])
        return
