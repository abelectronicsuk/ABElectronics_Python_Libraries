#!/usr/bin/python

import smbus
import re


# ================================================
# ABElectroncs IO Pi V2 32-Channel Port Expander
# Version 1.0 Created 01/02/2014
#
# Requires python smbus to be installed
# 
# ================================================

class IOPI :
  # Define registers values from datasheet
  IODIRA = 0x00 # Pin direction
  IODIRB = 0x01 # Pin direction
  OLATA = 0x14 # Outputs
  OLATB = 0x15 # Outputs
  GPIOA = 0x12 # Inputs
  GPIOB = 0x13 # Inputs
  
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
  
  #init object with i2c address, default is 0x20, 0x21 for ADCoPi board
  def __init__(self, address=0x20,inputmodeA=True, inputmodeB=True):
    self.address = address
    self.inputmodeA = inputmodeA
    self.inputmodeB = inputmodeB
    if inputmodeA == True:
      bus.write_byte_data(self.address,self.IODIRA,0x00)
      bus.write_byte_data(self.address,self.OLATA,0)
    else:
      bus.write_byte_data(self.address,self.IODIRA,0xFF)
    if inputmodeB == True:
      bus.write_byte_data(self.address,self.IODIRB,0x00)
      bus.write_byte_data(self.address,self.OLATB,0)
    else:
      bus.write_byte_data(self.address,self.IODIRB,0xFF)
    
  def setData(self,data,bank):
    if bank == 1:
     bus.write_byte_data(self.address,0x12,data)
    else:
     bus.write_byte_data(self.address,0x13,data)
    return
    
  def readData(self, bank):
    if bank == 1:
      return bus.read_byte_data(self.address,self.GPIOA)
    else:
      return bus.read_byte_data(self.address,self.GPIOA)
    
   