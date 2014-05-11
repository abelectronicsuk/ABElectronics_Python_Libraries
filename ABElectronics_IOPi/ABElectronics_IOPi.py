#!/usr/bin/python

import smbus
import re


# ================================================
# ABElectronics IO Pi 32-Channel Port Expander
# Version 1.1 Created 30/04/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# 
# ================================================

#
# Each MCP23017 chip is split into two 8-bit ports.  port 0 controls pins 1 to 8 while port 1 controls pins 9 to 16. 
# When writing to or reading from a port the least significant bit represents the lowest numbered pin on the selected port. 
# 

class IOPI :
  # Define registers values from datasheet
  IODIRA = 0x00 # IO direction A - 1= input 0 = output
  IODIRB = 0x01 # IO direction B - 1= input 0 = output
  IPOLA = 0x02 # Input polarity A - If a bit is set, the corresponding GPIO register bit will reflect the inverted value on the pin.
  IPOLB = 0x03 # Input polarity B - If a bit is set, the corresponding GPIO register bit will reflect the inverted value on the pin.
  GPINTENA = 0x04 # The GPINTEN register controls the interrupt-onchange feature for each pin on port A.
  GPINTENB = 0x05 # The GPINTEN register controls the interrupt-onchange feature for each pin on port B.
  DEFVALA = 0x06 # Default value for port A - These bits set the compare value for pins configured for interrupt-on-change. If the associated pin level is the opposite from the register bit, an interrupt occurs.
  DEFVALB = 0x07 # Default value for port B - These bits set the compare value for pins configured for interrupt-on-change. If the associated pin level is the opposite from the register bit, an interrupt occurs.
  INTCONA = 0x08 # Interrupt control register for port A.  If 1 interrupt is fired when the pin matches the default value, if 0 the interrupt is fired on state change
  INTCONB = 0x09 # Interrupt control register for port B.  If 1 interrupt is fired when the pin matches the default value, if 0 the interrupt is fired on state change
  IOCON = 0x0A # see datasheet for configuration register
  GPPUA = 0x0C # pull-up resistors for port A
  GPPUB = 0x0D # pull-up resistors for port B
  INTFA = 0x0E # The INTF register reflects the interrupt condition on the port A pins of any pin that is enabled for interrupts. A set bit indicates that the associated pin caused the interrupt.
  INTFB = 0x0F # The INTF register reflects the interrupt condition on the port B pins of any pin that is enabled for interrupts. A set bit indicates that the associated pin caused the interrupt.
  INTCAPA = 0x10 #The INTCAP register captures the GPIO port A value at the time the interrupt occurred.
  INTCAPB = 0x11 #The INTCAP register captures the GPIO port B value at the time the interrupt occurred.
  GPIOA = 0x12 # data port A
  GPIOB = 0x13 # data port B
  OLATA = 0x14 # output latches A
  OLATB = 0x15 # output latches B
  

  # variables
  address = 0x20 # I2C address
  portA_dir = 0x00 #port a direction
  portB_dir = 0x00 #port b direction
  portA_val = 0x00 #port a value
  portB_val = 0x00 #port b value
  portA_pullup = 0x00 #port a pull-up resistors
  portB_pullup = 0x00 #port a pull-up resistors
  portA_polarity = 0x00 #input polarity for port a
  portB_polarity = 0x00 #input polarity for port b
  intA = 0x00 #interrupt control for port a
  intB = 0x00 #interrupt control for port a
  config = 0x22 #initial configuration - see IOCON page in the MCP23017 datasheet for more information.
  
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
  
  
  def __init__(self, address=0x20):
    #init object with i2c address, default is 0x20, 0x21 for IOPi board, load default configuration, set all pins low and to output
    self.address = address
    bus.write_byte_data(self.address,self.IOCON,self.config)
    bus.write_byte_data(self.address,self.GPIOA,0x00)
    bus.write_byte_data(self.address,self.GPIOB,0x00)
    bus.write_byte_data(self.address,self.IODIRA,0x00)
    bus.write_byte_data(self.address,self.IODIRB,0x00)
    return
    
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

  #public methods

  def setPinDirection(self, pin, direction): 
      # set IO direction for an individual pin
      # pins 1 to 16
      # direction 1 = input, 0 = output
      pin = pin - 1;
      if pin < 8:
        self.portA_val = self.__updatebyte(self.portA_val, pin, direction)    
        bus.write_byte_data(self.address,self.IODIRA,self.portA_val)        
      else:
        self.portB_val = self.__updatebyte(self.portB_val, pin - 8, direction)       
        bus.write_byte_data(self.address,self.IODIRB,self.portB_val)
      return


  def setPortDirection(self, port, direction): 
      # set direction for an IO port
      #port 0 = pins 1 to 8, port 1 = pins 8 to 16 
      # 1 = input, 0 = output           
      if port == 1:
        bus.write_byte_data(self.address,self.IODIRB,direction)
        portB_dir = direction
      else:
        bus.write_byte_data(self.address,self.IODIRA,direction)
        portA_dir = direction
      return


  def setPinPullup(self, pin, value): 
      # set the internal 100K pull-up resistors for an individual pin
      # pins 1 to 16
      # value 1 = enabled, 0 = disabled
      pin = pin - 1;
      if pin < 8:
        self.portA_pullup = self.__updatebyte(self.portA_val, pin, value)    
        bus.write_byte_data(self.address,self.GPPUA,self.portA_pullup)        
      else:
        self.portB_pullup = self.__updatebyte(self.portB_val, pin - 8, value)       
        bus.write_byte_data(self.address,self.GPPUB,self.portB_pullup)
      return


  def setPortPullups(self, port, value): 
      # set the internal 100K pull-up resistors for the selected IO port
      if port == 1:
        self.portA_pullup = value
        bus.write_byte_data(self.address,self.GPPUB,value)
      else:
        self.portB_pullup = value
        bus.write_byte_data(self.address,self.GPPUA,value)
      return


  def writePin(self, pin, value): 
      # write to an individual pin 1 - 16
      pin = pin - 1;
      if pin < 8:
        self.portA_val = self.__updatebyte(self.portA_val, pin, value)    
        bus.write_byte_data(self.address,self.GPIOA,self.portA_val)        
      else:
        self.portB_val = self.__updatebyte(self.portB_val, pin - 8, value)       
        bus.write_byte_data(self.address,self.GPIOB,self.portB_val)
      return


  def writePort(self, port, value):
      # write to all pins on the selected port
      # port 0 = pins 1 to 8, port 1 = pins 8 to 16
      # value = number between 0 and 255 or 0x00 and 0xFF
      if port == 1:
        bus.write_byte_data(self.address,self.GPIOB,value)
        portB_val = value
      else:
        bus.write_byte_data(self.address,self.GPIOA,value)
        portA_val = value
      return


  def readPin(self, pin):
      # read the value of an individual pin 1 - 16
      # returns 0 = logic level low, 1 = logic level high
      pin = pin - 1;
      if pin < 8:
        portA_val = bus.read_byte_data(self.address,self.GPIOA)  
        return self.__checkbit(portA_val, pin)
      else:
        pin = pin - 8
        portB_val = bus.read_byte_data(self.address,self.GPIOB)     
        return self.__checkbit(portB_val, pin)


  def readPort(self, port):
      # read all pins on the selected port
      # port 0 = pins 1 to 8, port 1 = pins 8 to 16
      # returns number between 0 and 255 or 0x00 and 0xFF
      if port == 1:
        portB_val = bus.read_byte_data(self.address,self.GPIOB)
        return portB_val
      else:
        portA_val = bus.read_byte_data(self.address,self.GPIOA)
        return portA_val
      
  def invertPort(self, port, polarity): 
      # invert the polarity of the pins on a selected port
      # port 0 = pins 1 to 8, port 1 = pins 8 to 16
      # polarity 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
      if port == 1:
        bus.write_byte_data(self.address,self.IPOLB,value)
        portB_polarity = value
      else:
        bus.write_byte_data(self.address,self.IPOLA,value)
        portA_polarity = value
      return

  def invertPin(self, pin, polarity):
      #invert the polarity of the selected pin
      #pins 1 to 16
      #polarity 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
      pin = pin - 1;
      if pin < 8:
        self.portA_polarity = self.__updatebyte(self.portA_val, pin, polarity)    
        bus.write_byte_data(self.address,self.IPOLA,self.portA_polarity)        
      else:
        self.portB_polarity = self.__updatebyte(self.portB_val, pin - 8, polarity)       
        bus.write_byte_data(self.address,self.IPOLB,self.portB_polarity)
      return

  def mirrorInterrupts(self, value): 
      # 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INTA is associated with PortA and INTB is associated with PortB
      if value == 0:
          self.config = self.__updatebyte(self.config, 6, 0)
          bus.write_byte_data(self.address,self.IOCON,self.config)
      if value == 1:
          self.config = self.__updatebyte(self.config, 6, 1)
          bus.write_byte_data(self.address,self.IOCON,self.config)
      return

  def setInterruptPolarity(self, value): 
      # This sets the polarity of the INT output pins - 1 = Active-high. 0 = Active-low.
      if value == 0:
          self.config = self.__updatebyte(self.config, 1, 0)
          bus.write_byte_data(self.address,self.IOCON,self.config)
      if value == 1:
          self.config = self.__updatebyte(self.config, 1, 1)
          bus.write_byte_data(self.address,self.IOCON,self.config)
      return
      return

  def setInterruptType(self, port, value):
      #Sets the type of interrupt for each pin on the selected port
      #1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change
      if port == 0:
        bus.write_byte_data(self.address,self.INTCONA,value)
      else:
        bus.write_byte_data(self.address,self.INTCONB,value)
      return

  def setInterruptDefaults(self, port, value):
      #These bits set the compare value for pins configured for interrupt-on-change on the selected port. 
      #If the associated pin level is the opposite from the register bit, an interrupt occurs.
      if port == 0:
        bus.write_byte_data(self.address,self.DEFVALA,value)
      else:
        bus.write_byte_data(self.address,self.DEFVALB,value)
      return


  def setInterruptOnPort(self, port, value):
      # Enable interrupts for the pins on the selected port
      # port 0 = pins 1 to 8, port 1 = pins 8 to 16
      # value = number between 0 and 255 or 0x00 and 0xFF
      if port == 0:
        bus.write_byte_data(self.address,self.GPINTENA,value)
        self.intA = value
      else:
        bus.write_byte_data(self.address,self.GPINTENB,value)
        self.intB = value
      return

  def setInterruptOnPin(self, pin, value):
      # Enable interrupts for the selected pin
      # Pin = 1 to 16
      # Value 0 = interrupt disabled, 1 = interrupt enabled
      pin = pin - 1;
      if pin < 8:
        self.intA = self.__updatebyte(self.intA, pin, value)    
        bus.write_byte_data(self.address,self.GPINTENA,self.intA)        
      else:
        self.intB = self.__updatebyte(self.intB, pin - 8, value)       
        bus.write_byte_data(self.address,self.GPINTENB,self.intB)
      return

  def readInterruptStatus(self, port): 
      # read the interrupt status for the pins on the selected port
      # port 0 = pins 1 to 8, port 1 = pins 8 to 16
      if port == 0:
        return bus.read_byte_data(self.address,self.INTFA)
      else:
        return bus.read_byte_data(self.address,self.INTFB)
      

  def readInterruptCature(self, port): 
      # read the value from the selected port at the time of the last interrupt trigger
      #port 0 = pins 1 to 8, port 1 = pins 8 to 16
      if port == 0:
        return bus.read_byte_data(self.address,self.INTCAPA)
      else:
        return bus.read_byte_data(self.address,self.INTCAPB)

  def resetInterrupts(self):
      # set the interrupts A and B to 0
      self.readInterruptCature(0)
      self.readInterruptCature(1)
      return




   