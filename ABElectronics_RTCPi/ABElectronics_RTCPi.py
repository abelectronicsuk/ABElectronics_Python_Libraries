#!/usr/bin/python

import smbus
import datetime
import re


# ================================================
# ABElectronics RTC Pi Real-time clock
# Version 1.0 Created 01/05/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# 
# ================================================

#
# Based on the Maxim DS1307 
# When writing to or reading from a port the least significant bit represents the lowest numbered pin on the selected port. 
# 

class RTC :
  # Define registers values from datasheet
  SECONDS = 0x00 # 
  MINUTES = 0x01 # 
  HOURS = 0x02 # 
  DAYOFWEEK = 0x03 # 
  DAY = 0x04 # 
  MONTH = 0x05 # 
  YEAR = 0x06 # 
  CONTROL = 0x07 # 
    
  # variables
  __rtcAddress = 0x68 # I2C address  
  __config = 0x03 #initial configuration - square wave and output disabled, frequency set to 32.768KHz.
  __century = 2000 # the DS1307 does not store the current century so that has to be added on manually.

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

  # local methods    

  def __init__(self):
    bus.write_byte_data(self.__rtcAddress,self.CONTROL,self.__config)
    return

  def __BCDtoDec(self, x):
     return x - 6 * (x >> 4)

  def __DecToBcd(self, val):
    return ( (val/10*16) + (val%10) )

  def __getCentury(self, val):
    if len(val) > 2:
        y = val[0] + val[1]
        self.__century = int(y) * 100
    return

  def __updatebyte(self, byte, bit, value): 
      # internal method for setting the value of a single bit within a byte
    if value == 0:
        return byte & ~(1 << bit)
    elif value == 1:
        return byte | (1 << bit)

  # public methods
  def setDate(self, date):
    # set the date and time on the RTC
    # date must be in ISO 8601 format - YYYY-MM-DDTHH:MM:SS 
    d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S" )
    self.__getCentury(date)
    bus.write_byte_data(self.__rtcAddress,self.SECONDS, self.__DecToBcd(d.second)) 
    bus.write_byte_data(self.__rtcAddress,self.MINUTES, self.__DecToBcd(d.minute)) 
    bus.write_byte_data(self.__rtcAddress,self.HOURS, self.__DecToBcd(d.hour)) 
    bus.write_byte_data(self.__rtcAddress,self.DAYOFWEEK, self.__DecToBcd(d.weekday())) 
    bus.write_byte_data(self.__rtcAddress,self.DAY,  self.__DecToBcd(d.day)) 
    bus.write_byte_data(self.__rtcAddress,self.MONTH,  self.__DecToBcd(d.month)) 
    bus.write_byte_data(self.__rtcAddress,self.YEAR, self.__DecToBcd(d.year - self.__century)) 
    return

  def readDate(self):
    # read the date and time from the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS 
    seconds, minutes, hours, dayofweek, day, month, year = bus.read_i2c_block_data(self.__rtcAddress, 0, 7)
    date = ("%02d-%02d-%02dT%02d:%02d:%02d " % (self.__BCDtoDec(year) + self.__century, self.__BCDtoDec(month), self.__BCDtoDec(day),self.__BCDtoDec(hours), self.__BCDtoDec(minutes), self.__BCDtoDec(seconds)))
    return date

  def enableOutput(self):
    # Enable the output pin
    self.__config = self.__updatebyte(self.__config, 7, 1)
    self.__config = self.__updatebyte(self.__config, 4, 1)
    bus.write_byte_data(self.__rtcAddress,self.CONTROL,self.__config)
    return

  def disableOutput(self):
    # Disable the output pin
    self.__config = self.__updatebyte(self.__config, 7, 0)
    self.__config = self.__updatebyte(self.__config, 4, 0)
    bus.write_byte_data(self.__rtcAddress,self.CONTROL,self.__config)
    return

  def setFrequency(self, frequency):
    # set the frequency of the output pin square-wave
    # options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
    if frequency == 1:
        self.__config = self.__updatebyte(self.__config, 0, 0)
        self.__config = self.__updatebyte(self.__config, 1, 0)
    if frequency == 2:
        self.__config = self.__updatebyte(self.__config, 0, 1)
        self.__config = self.__updatebyte(self.__config, 1, 0)
    if frequency == 3:
        self.__config = self.__updatebyte(self.__config, 0, 0)
        self.__config = self.__updatebyte(self.__config, 1, 1)
    if frequency == 4:
        self.__config = self.__updatebyte(self.__config, 0, 1)
        self.__config = self.__updatebyte(self.__config, 1, 1)
    bus.write_byte_data(self.__rtcAddress,self.CONTROL,self.__config)
    return