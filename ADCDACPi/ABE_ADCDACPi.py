#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev
import ctypes

"""
================================================
ABElectronics ADCDAC Pi Analogue to Digital / Digital to Analogue Converter
Version 1.0 Created 16/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Version 1.2 5/9/2015 Added controllable gain factor
================================================

Based on the Microchip MCP3202 and MCP4822
"""

class Dac_bits(ctypes.LittleEndianStructure):
    """Class to define the DAC command register bitfields.

    See Microchip mcp4822 datasheet for more information
    """
    _fields_ = [
                   ("data", ctypes.c_uint16, 12), #Bits 0:11
                   ("shutdown", ctypes.c_uint16, 1), #Bit 12
                   ("gain", ctypes.c_uint16, 1), #Bit 13
                   ("reserved1", ctypes.c_uint16, 1), #Bit 14
                   ("channel", ctypes.c_uint16, 1) #Bit 15
               ]

    #GA field value lookup. <gainFactor>:<bitfield val>
    __ga_field__ = {1:1, 2:0}
    def gain_to_field_val(self, gainFactor):
        """Returns bitfield value based on desired gain"""
        return self.__ga_field__[gainFactor]

class Dac_register(ctypes.Union):
    """Union to represent the DAC's command register

    See Microchip mcp4822 datasheet for more information
    """
    _fields_ = [
                   ("bits", Dac_bits),
                   ("bytes", ctypes.c_uint8 * 2),
                   ("reg", ctypes.c_uint16)
               ]

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
    def __init__(self, gainFactor = 1):
        """Class Constructor

        gainFactor -- Set the DAC's gain factor. The value should
           be 1 or 2.  Gain factor is used to determine output voltage
           from the formula: Vout = G * Vref * D/4096
           Where G is gain factor, Vref (for this chip) is 2.048 and
           D is the 12-bit digital value
        """
        if (gainFactor != 1) and (gainFactor != 2):
            print 'Invalid gain factor. Must be 1 or 2'
            self.gain = 1
        else:
            self.gain = gainFactor

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
        if (voltage >= 0.0) and (voltage < self.__adcrefvoltage):
            rawval = (voltage / 2.048) * 4096 / self.gain
            self.set_dac_raw(channel, int(rawval))
        return

    def set_dac_raw(self, channel, value):
        """
        Set the raw value from the selected channel on the DAC
        Channel = 1 or 2
        Value between 0 and 4095
        """
        reg = Dac_register()

        #Configurable fields
        reg.bits.data = value
        reg.bits.channel = channel - 1
        reg.bits.gain = reg.bits.gain_to_field_val(self.gain)

        #Fixed fields:
        reg.bits.shutdown = 1 #Active low

        #Write to device
        self.spiDAC.xfer2( [ reg.bytes[1], reg.bytes[0] ])
        return
