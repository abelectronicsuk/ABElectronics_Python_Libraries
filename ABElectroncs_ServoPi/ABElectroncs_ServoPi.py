#!/usr/bin/python

import time
import math
import smbus
import re
import RPi.GPIO as GPIO


# ================================================
# ABElectroncs ServoPi 16-Channel PWM Servo Driver
#
# Requires python smbus to be installed
# ================================================

class PWM :
  # Define registers values from datasheet
  MODE1              = 0x00
  MODE2              = 0x01
  SUBADR1            = 0x02
  SUBADR2            = 0x03
  SUBADR3            = 0x04
  ALLCALLADR         = 0x05
  LED0_ON_L          = 0x06
  LED0_ON_H          = 0x07
  LED0_OFF_L         = 0x08
  LED0_OFF_H         = 0x09
  ALL_LED_ON_L        = 0xFA
  ALL_LED_ON_H        = 0xFB
  ALL_LED_OFF_L       = 0xFC
  ALL_LED_OFF_H       = 0xFD
  PRE_SCALE           = 0xFE
  
  
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
  
  #init object with i2c address, default is 0x40 for ServoPi board
  def __init__(self, address=0x40):
    self.address = address
    write(self.address, self.MODE1, 0x00)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)


  # Set the PWM frequency
  def setPWMFreq(self, freq):
    scaleval = 25000000.0    # 25MHz
    scaleval /= 4096.0       # 12-bit
    scaleval /= float(freq)
    scaleval -= 1.0
    prescale = math.floor(scaleval + 0.5)
    oldmode = read(self.address, self.MODE1);
    newmode = (oldmode & 0x7F) | 0x10
    write(self.address,self.MODE1, newmode)
    write(self.address,self.PRE_SCALE, int(math.floor(prescale)))
    write(self.address,self.MODE1, oldmode)
    time.sleep(0.005)
    write(self.address,self.MODE1, oldmode | 0x80)
  
  # set the output on a single channel
  def setPWM(self,channel, on, off):
    write(self.address,self.LED0_ON_L+4*channel, on & 0xFF)
    write(self.address,self.LED0_ON_H+4*channel, on >> 8)
    write(self.address,self.LED0_OFF_L+4*channel, off & 0xFF)
    write(self.address,self.LED0_OFF_H+4*channel, off >> 8)
    
# set the output on all channels
  def setAllPWM(self,channel, on, off):
    write(self.address,self.ALL_LED_ON_L+4*channel, on & 0xFF)
    write(self.address,self.ALL_LED_ON_H+4*channel, on >> 8)
    write(self.address,self.ALL_LED_OFF_L+4*channel, off & 0xFF)
    write(self.address,self.ALL_LED_OFF_H+4*channel, off >> 8)

# Write data to I2C bus
def write(address,reg, value):
    try:
      bus.write_byte_data(address, reg, value)
    except IOError, err:
      return self.errMsg()


# Read data from I2C bus
def read(address, reg):
    try:
      result = bus.read_byte_data(address, reg)
      return result
    except IOError, err:
      return self.errMsg()

# disable output via OE pin
def outputDisable():
  GPIO.output(7, True)
  
# enable output via OE pin
def outputEnable():
  GPIO.output(7, False)  