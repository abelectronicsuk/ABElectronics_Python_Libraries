#!/usr/bin/python

import smbus
import re


# ================================================
# ABElectronics ADC Pi V2 8-Channel ADC
# Version 1.0 Created 01/02/2014
#
# Requires python smbus to be installed
# ADC Gain  = 1
# ================================================

class ADC :
  # Define registers values from datasheet
  CHANNEL1_18BIT	= 0x9C
  CHANNEL2_18BIT	= 0xBC
  CHANNEL3_18BIT	= 0xDC
  CHANNEL4_18BIT	= 0xFC
  DIVISIOR_18BIT	= 64

  CHANNEL1_16BIT	= 0x98
  CHANNEL2_16BIT	= 0xB8
  CHANNEL3_16BIT	= 0xD8
  CHANNEL4_16BIT	= 0xF8
  DIVISIOR_16BIT	= 16
  
  CHANNEL1_12BIT	= 0x90
  CHANNEL2_12BIT	= 0xB0
  CHANNEL3_12BIT	= 0xD0
  CHANNEL4_12BIT	= 0xF0
  DIVISIOR_12BIT	= 1
  
  # create byte array and fill with initial values to define size
  adcreading = bytearray()
  
  adcreading.append(0x00)
  adcreading.append(0x00)
  adcreading.append(0x00)
  adcreading.append(0x00)

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
  
  #init object with i2c address, default is 0x68, 0x69 for ADCoPi board
  def __init__(self, address=0x68, address2=0x69, bitrate=18):
    self.address = address
    self.address2 = address2
    self.bitrate = bitrate
    

  def GetChannelConfig(self, channel):
    if (self.bitrate == 18):
      if (channel == 1 or channel == 5):
        return self.CHANNEL1_18BIT
      if (channel == 2 or channel == 6):
        return self.CHANNEL2_18BIT
      if (channel == 3 or channel == 7):
        return self.CHANNEL3_18BIT
      if (channel == 4 or channel == 8):
        return self.CHANNEL4_18BIT
        
    if (self.bitrate == 16):
      if (channel == 1 or channel == 5):
        return self.CHANNEL1_16BIT
      if (channel == 2 or channel == 6):
        return self.CHANNEL2_16BIT
      if (channel == 3 or channel == 7):
        return self.CHANNEL3_16BIT
      if (channel == 4 or channel == 8):
        return self.CHANNEL4_16BIT   
        
    if (self.bitrate == 12):
      if (channel == 1 or channel == 5):
        return self.CHANNEL1_12BIT
      if (channel == 2 or channel == 6):
        return self.CHANNEL2_12BIT
      if (channel == 3 or channel == 7):
        return self.CHANNEL3_12BIT
      if (channel == 4 or channel == 8):
        return self.CHANNEL4_12BIT
        

  def changechannel(self, channel):
    if (channel < 5):
      tmp= bus.write_byte(self.address, self.GetChannelConfig(channel))
    else:
      tmp= bus.write_byte(self.address2, self.GetChannelConfig(channel))

  def getadcreading(self, channel):
    if (channel < 5):
      I2CAddress= self.address
    else:
      I2CAddress= self.address2
      
    adcConfig = self.GetChannelConfig(channel)
    if (self.bitrate == 18):
      varMultiplier = (2.4705882/self.DIVISIOR_18BIT)/1000
    if (self.bitrate == 16):
      varMultiplier = (2.4705882/self.DIVISIOR_16BIT)/1000
    if (self.bitrate == 12):
      varMultiplier = (2.4705882/self.DIVISIOR_12BIT)/1000  
      
    if (self.bitrate == 18):
      adcreading = bus.read_i2c_block_data(I2CAddress,adcConfig)
      h = adcreading[0]
      m = adcreading[1]
      l = adcreading[2]
      s = adcreading[3]
      # wait for new data
      while (s & 128):
        adcreading = bus.read_i2c_block_data(I2CAddress,adcConfig)
        h = adcreading[0]
        m = adcreading[1]
        l = adcreading[2]
        s = adcreading[3]
	
      # shift bits to product result
      t = ((h & 0b00000001) << 16) | (m << 8) | l
      # check if positive or negative number and invert if needed
      if (h > 128):
        t = ~(0x020000 - t)
      return t * varMultiplier
      
    # is 16 or 12 bit mode  
    else:
    
      adcreading = bus.read_i2c_block_data(I2CAddress,adcConfig)
      h = adcreading[0]
      l = adcreading[1]
      s = adcreading[2]
    	
      # wait for new data
      while (s & 128):
        adcreading = bus.read_i2c_block_data(I2CAddress,adcConfig)
    	h = adcreading[0]
    	l = adcreading[1]
    	s = adcreading[2]
    		
    	
      # shift bits to product result
      t = (h << 8) | l
      # check if positive or negative number and invert if needed
      if (h > 128):
        t = ~(0x020000 - t)
      return t * varMultiplier