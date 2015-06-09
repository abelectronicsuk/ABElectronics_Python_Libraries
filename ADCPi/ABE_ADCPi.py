#!/usr/bin/python

"""
================================================
ABElectronics ADC Pi V2 8-Channel ADC
Version 1.0 Created 09/05/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format
Requires python smbus to be installed

================================================
"""


class ADCPi:
    # internal variables

    __address = 0x68  # default address for adc 1 on adc pi and delta-sigma pi
    __address2 = 0x69  # default address for adc 2 on adc pi and delta-sigma pi
    __config1 = 0x9C  # PGAx1, 18 bit, continuous conversion, channel 1
    __currentchannel1 = 1  # channel variable for adc 1
    __config2 = 0x9C  # PGAx1, 18 bit, continuous-shot conversion, channel 1
    __currentchannel2 = 1  # channel variable for adc2
    __bitrate = 18  # current bitrate
    __conversionmode = 1 # Conversion Mode
    __pga = float(0.5)  # current pga setting
    __lsb = float(0.0000078125)  # default lsb value for 18 bit

    # create byte array and fill with initial values to define size
    __adcreading = bytearray()
    __adcreading.append(0x00)
    __adcreading.append(0x00)
    __adcreading.append(0x00)
    __adcreading.append(0x00)

    global _bus

    # local methods

    def __updatebyte(self, byte, bit, value):
            # internal method for setting the value of a single bit within a
            # byte
        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    def __checkbit(self, byte, bit):
            # internal method for reading the value of a single bit within a
            # byte
        bitval = ((byte & (1 << bit)) != 0)
        if (bitval == 1):
            return True
        else:
            return False

    def __twos_comp(self, val, bits):
        if((val & (1 << (bits - 1))) != 0):
            val = val - (1 << bits)
        return val

    def __setchannel(self, channel):
        # internal method for updating the config to the selected channel
        if channel < 5:
            if channel != self.__currentchannel1:
                if channel == 1:
                    self.__config1 = self.__updatebyte(self.__config1, 5, 0)
                    self.__config1 = self.__updatebyte(self.__config1, 6, 0)
                    self.__currentchannel1 = 1
                if channel == 2:
                    self.__config1 = self.__updatebyte(self.__config1, 5, 1)
                    self.__config1 = self.__updatebyte(self.__config1, 6, 0)
                    self.__currentchannel1 = 2
                if channel == 3:
                    self.__config1 = self.__updatebyte(self.__config1, 5, 0)
                    self.__config1 = self.__updatebyte(self.__config1, 6, 1)
                    self.__currentchannel1 = 3
                if channel == 4:
                    self.__config1 = self.__updatebyte(self.__config1, 5, 1)
                    self.__config1 = self.__updatebyte(self.__config1, 6, 1)
                    self.__currentchannel1 = 4
        else:
            if channel != self.__currentchannel2:
                if channel == 5:
                    self.__config2 = self.__updatebyte(self.__config2, 5, 0)
                    self.__config2 = self.__updatebyte(self.__config2, 6, 0)
                    self.__currentchannel2 = 5
                if channel == 6:
                    self.__config2 = self.__updatebyte(self.__config2, 5, 1)
                    self.__config2 = self.__updatebyte(self.__config2, 6, 0)
                    self.__currentchannel2 = 6
                if channel == 7:
                    self.__config2 = self.__updatebyte(self.__config2, 5, 0)
                    self.__config2 = self.__updatebyte(self.__config2, 6, 1)
                    self.__currentchannel2 = 7
                if channel == 8:
                    self.__config2 = self.__updatebyte(self.__config2, 5, 1)
                    self.__config2 = self.__updatebyte(self.__config2, 6, 1)
                    self.__currentchannel2 = 8
        return

    # init object with i2caddress, default is 0x68, 0x69 for ADCoPi board
    def __init__(self, bus, address=0x68, address2=0x69, rate=18):
        self._bus = bus
        self.__address = address
        self.__address2 = address2
        self.set_bit_rate(rate)

    def read_voltage(self, channel):
        # returns the voltage from the selected adc channel - channels 1 to
        # 8
        raw = self.read_raw(channel)
        if (self.__signbit):
            return float(0.0)  # returned a negative voltage so return 0
        else:
            voltage = float(
                (raw * (self.__lsb / self.__pga)) * 2.471)
            return float(voltage)

    def read_raw(self, channel):
        # reads the raw value from the selected adc channel - channels 1 to 8
        h = 0
        l = 0
        m = 0
        s = 0

        # get the config and i2c address for the selected channel
        self.__setchannel(channel)
        if (channel < 5):            
            config = self.__config1
            address = self.__address
        else:
            config = self.__config2
            address = self.__address2
            
        # if the conversion mode is set to one-shot update the ready bit to 1
        if (self.__conversionmode == 0):
                config = self.__updatebyte(config, 7, 1)
                self._bus.write_byte(address, config)
                config = self.__updatebyte(config, 7, 0)
        # keep reading the adc data until the conversion result is ready
        while True:
            
            __adcreading = self._bus.read_i2c_block_data(address, config, 4)
            if self.__bitrate == 18:
                h = __adcreading[0]
                m = __adcreading[1]
                l = __adcreading[2]
                s = __adcreading[3]
            else:
                h = __adcreading[0]
                m = __adcreading[1]
                s = __adcreading[2]
            if self.__checkbit(s, 7) == 0:
                break

        self.__signbit = False
        t = 0.0
        # extract the returned bytes and combine in the correct order
        if self.__bitrate == 18:
            t = ((h & 0b00000011) << 16) | (m << 8) | l
            self.__signbit = bool(self.__checkbit(t, 17))
            if self.__signbit:
                t = self.__updatebyte(t, 17, 0)

        if self.__bitrate == 16:
            t = (h << 8) | m
            self.__signbit = bool(self.__checkbit(t, 15))
            if self.__signbit:
                t = self.__updatebyte(t, 15, 0)

        if self.__bitrate == 14:
            t = ((h & 0b00111111) << 8) | m
            self.__signbit = self.__checkbit(t, 13)
            if self.__signbit:
                t = self.__updatebyte(t, 13, 0)

        if self.__bitrate == 12:
            t = ((h & 0b00001111) << 8) | m
            self.__signbit = self.__checkbit(t, 11)
            if self.__signbit:
                t = self.__updatebyte(t, 11, 0)

        return t

    def set_pga(self, gain):
        """
        PGA gain selection
        1 = 1x
        2 = 2x
        4 = 4x
        8 = 8x
        """

        if gain == 1:
            self.__config1 = self.__updatebyte(self.__config1, 0, 0)
            self.__config1 = self.__updatebyte(self.__config1, 1, 0)
            self.__config2 = self.__updatebyte(self.__config2, 0, 0)
            self.__config2 = self.__updatebyte(self.__config2, 1, 0)
            self.__pga = 0.5
        if gain == 2:
            self.__config1 = self.__updatebyte(self.__config1, 0, 1)
            self.__config1 = self.__updatebyte(self.__config1, 1, 0)
            self.__config2 = self.__updatebyte(self.__config2, 0, 1)
            self.__config2 = self.__updatebyte(self.__config2, 1, 0)
            self.__pga = 1
        if gain == 4:
            self.__config1 = self.__updatebyte(self.__config1, 0, 0)
            self.__config1 = self.__updatebyte(self.__config1, 1, 1)
            self.__config2 = self.__updatebyte(self.__config2, 0, 0)
            self.__config2 = self.__updatebyte(self.__config2, 1, 1)
            self.__pga = 2
        if gain == 8:
            self.__config1 = self.__updatebyte(self.__config1, 0, 1)
            self.__config1 = self.__updatebyte(self.__config1, 1, 1)
            self.__config2 = self.__updatebyte(self.__config2, 0, 1)
            self.__config2 = self.__updatebyte(self.__config2, 1, 1)
            self.__pga = 4

        self._bus.write_byte(self.__address, self.__config1)
        self._bus.write_byte(self.__address2, self.__config2)
        return

    def set_bit_rate(self, rate):
        """
        sample rate and resolution
        12 = 12 bit (240SPS max)
        14 = 14 bit (60SPS max)
        16 = 16 bit (15SPS max)
        18 = 18 bit (3.75SPS max)
        """

        if rate == 12:
            self.__config1 = self.__updatebyte(self.__config1, 2, 0)
            self.__config1 = self.__updatebyte(self.__config1, 3, 0)
            self.__config2 = self.__updatebyte(self.__config2, 2, 0)
            self.__config2 = self.__updatebyte(self.__config2, 3, 0)
            self.__bitrate = 12
            self.__lsb = 0.0005
        if rate == 14:
            self.__config1 = self.__updatebyte(self.__config1, 2, 1)
            self.__config1 = self.__updatebyte(self.__config1, 3, 0)
            self.__config2 = self.__updatebyte(self.__config2, 2, 1)
            self.__config2 = self.__updatebyte(self.__config2, 3, 0)
            self.__bitrate = 14
            self.__lsb = 0.000125
        if rate == 16:
            self.__config1 = self.__updatebyte(self.__config1, 2, 0)
            self.__config1 = self.__updatebyte(self.__config1, 3, 1)
            self.__config2 = self.__updatebyte(self.__config2, 2, 0)
            self.__config2 = self.__updatebyte(self.__config2, 3, 1)
            self.__bitrate = 16
            self.__lsb = 0.00003125
        if rate == 18:
            self.__config1 = self.__updatebyte(self.__config1, 2, 1)
            self.__config1 = self.__updatebyte(self.__config1, 3, 1)
            self.__config2 = self.__updatebyte(self.__config2, 2, 1)
            self.__config2 = self.__updatebyte(self.__config2, 3, 1)
            self.__bitrate = 18
            self.__lsb = 0.0000078125

        self._bus.write_byte(self.__address, self.__config1)
        self._bus.write_byte(self.__address2, self.__config2)
        return
    
    def set_conversion_mode(self, mode):
        """
        conversion mode for adc
        0 = One shot conversion mode
        1 = Continuous conversion mode
        """
        if (mode == 0):
            self.__config1 = self.__updatebyte(self.__config1, 4, 0)
            self.__config2 = self.__updatebyte(self.__config2, 4, 0)
            self.__conversionmode = 0
        if (mode == 1):
            self.__config1 = self.__updatebyte(self.__config1, 4, 1)
            self.__config2 = self.__updatebyte(self.__config2, 4, 1)
            self.__conversionmode = 1
        #self._bus.write_byte(self.__address, self.__config1)
        #self._bus.write_byte(self.__address2, self.__config2)    
        return
