#!/usr/bin/python

import smbus
import re


# ================================================
# ABElectronics ADC Pi V2 8-Channel ADC
# Version 1.0 Created 09/05/2014
#
# Requires python smbus to be installed
#
# ================================================

class ADCPi :
  # internal variables

  __address = 0x68 # default address for adc 1 on adc pi and delta-sigma pi
  __address2 = 0x69 # default address for adc 2 on adc pi and delta-sigma pi
  __config1 = 0x1C # PGAx1, 18 bit, one-shot conversion, channel 1
  __currentchannel1 = 1 # channel variable for adc 1
  __config2 = 0x1C # PGAx1, 18 bit, one-shot conversion, channel 1
  __currentchannel2 = 1 # channel variable for adc2
  __bitrate = 18 # current bitrate
  __pga = 0.48828125 # current pga setting
  __signbit = 0 # signed bit checker
  __lsb = 0.0000078125 # default lsb value for 18 bit

  
  # create byte array and fill with initial values to define size
  __adcreading = bytearray()  
  __adcreading.append(0x00)
  __adcreading.append(0x00)
  __adcreading.append(0x00)
  __adcreading.append(0x00)

  # detect i2C port number and assign to i2c_bus
  for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
      (name, value) = (m.group(1), m.group(2))
      if name == "Revision":
        if value [-4:] in ('0002', '0003'):
          i2c_bus = 0
        else:
          i2c_bus = 1
        break
  
    # Define I2C bus and init        
  global bus
  bus = smbus.SMBus(i2c_bus); 

  #local methods    

  def __updatebyte(self, byte, bit, value): 
      # internal method for setting the value of a single bit within a byte
    if value == 0:
        return byte & ~(1 << bit)
    elif value == 1:
        return byte | (1 << bit)


  def __checkbit(self, byte, bit): 
      # internal method for reading the value of a single bit within a byte
    if byte & (1 << bit):
        return 1
    else:
        return 0
  
  def __twos_comp(self, val, bits):
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
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
 
  #init object with i2caddress, default is 0x68, 0x69 for ADCoPi board
  def __init__(self, address=0x68, address2=0x69, rate=18):
    self.__address = address
    self.__address2 = address2
    self.setBitRate(rate)
    

  def readVoltage(self, channel): 
      # returns the voltage from the selected adc channel - channels 1 to 8
      if self.__signbit == 1: return 0 # returned a negative voltage so return 0  
      
      raw = self.readRaw(channel)
      voltage = (raw * (self.__lsb/self.__pga)) * 2.448579823702253

      return voltage

  
  def readRaw(self, channel): 
      # reads the raw value from the selected adc channel - channels 1 to 8
      
      self.__setchannel(channel) # get the config and i2c address for the selected channel
      if (channel < 5):
          config = self.__config1
          address = self.__address
      else:
          config = self.__config2
          address = self.__address2
      
      while 1:  # keep reading the adc data until the conversion result is ready
          __adcreading = bus.read_i2c_block_data(address,config)
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
              break;      
          
      self.__signbit = 0
      t = 0.0
      # extract the returned bytes and combine in the correct order
      if self.__bitrate == 18:
          t = ((h & 0b00000001) << 16) | (m << 8) | l
          if self.__checkbit(h, 1) == 1:
             self.__signbit = 1

      if self.__bitrate == 16:
          t = (h << 8) | m
          if self.__checkbit(h, 7) == 1:
             self.__signbit = 1
      
      if self.__bitrate == 14:
          t = ((h & 0b00011111) << 8) | m
          if self.__checkbit(h, 5) == 1:
             self.__signbit = 1

      if self.__bitrate == 12:
          t = ((h & 0b00000111) << 8) | m
          if self.__checkbit(h, 3) == 1:
             self.__signbit = 1
     
      return t


  def setPGA(self, gain):
      # PGA gain selection
      #1 = 1x
      #2 = 2x
      #4 = 4x
      #8 = 8x
      if gain == 1:
        self.__config1 = self.__updatebyte(self.__config1, 0, 0)
        self.__config1 = self.__updatebyte(self.__config1, 1, 0)
        self.__config2 = self.__updatebyte(self.__config2, 0, 0)
        self.__config2 = self.__updatebyte(self.__config2, 1, 0)
        self.__pga = 0.48828125
      if gain == 2:
        self.__config1 = self.__updatebyte(self.__config1, 0, 1)
        self.__config1 = self.__updatebyte(self.__config1, 1, 0)
        self.__config2 = self.__updatebyte(self.__config2, 0, 1)
        self.__config2 = self.__updatebyte(self.__config2, 1, 0)
        self.__pga = 0.9765625
      if gain == 4:
        self.__config1 = self.__updatebyte(self.__config1, 0, 0)
        self.__config1 = self.__updatebyte(self.__config1, 1, 1)
        self.__config2 = self.__updatebyte(self.__config2, 0, 0)
        self.__config2 = self.__updatebyte(self.__config2, 1, 1)
        self.__pga = 1.953125
      if gain == 8:
        self.__config1 = self.__updatebyte(self.__config1, 0, 1)
        self.__config1 = self.__updatebyte(self.__config1, 1, 1)
        self.__config2 = self.__updatebyte(self.__config2, 0, 1)
        self.__config2 = self.__updatebyte(self.__config2, 1, 1)
        self.__pga = 3.90625
       
      bus.write_byte(self.__address, self.__config1)
      bus.write_byte(self.__address2, self.__config2)
      return

  def setBitRate(self, rate): 
      # sample rate and resolution
      #12 = 12 bit (240SPS max)
      #14 = 14 bit (60SPS max)
      #16 = 16 bit (15SPS max)
      #18 = 18 bit (3.75SPS max)
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
       
      bus.write_byte(self.__address, self.__config1)
      bus.write_byte(self.__address2, self.__config2)
      return
                         