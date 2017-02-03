#!/usr/bin/python

"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tkinter GUI Demo
Version 1.0 Created 03/02/2017

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-guiwrite.py
================================================

This example creates a GUI using Tkinter with 16 buttons and uses the write_pin method 
to switch the pins on Bus 2 on the IO Pi on and off .

Initialises the IOPi device using the default addresse for Bus 2, you will need to
change the addresses if you have changed the jumpers on the IO Pi
"""


from Tkinter import *
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time



class App:
  global i2c_helper
  global newbus
  global bus2
  
  
  def __init__(self, master):
    self.i2c_helper = ABEHelpers()
    self.newbus = self.i2c_helper.get_smbus()
    self.bus2 = IoPi(self.newbus, 0x21) # create an instance of Bus 2 which is on I2C address 0x21 by default
    self.bus2.set_port_direction(0, 0x00) # set pins 1 to 8 to be outputs and turn them off
    self.bus2.write_port(0, 0x00)
    
    self.bus2.set_port_direction(1, 0x00) # set pins 9 to 16 to be outputs and turn them off
    self.bus2.write_port(1, 0x00)
    
    
    frame = Frame(master) # create a frame for the GUI
    frame.pack()
    
    # create 16 buttons which run the togglepin function when pressed
    self.button = Button(frame, 
                             text="Pin 1",command=lambda : self.togglepin(1))
    self.button.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 2",command=lambda : self.togglepin(2))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 3",command=lambda : self.togglepin(3))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 4",command=lambda : self.togglepin(4))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 5",command=lambda : self.togglepin(5))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 6",command=lambda : self.togglepin(6))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 7",command=lambda : self.togglepin(7))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 8",command=lambda : self.togglepin(8))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 9",command=lambda : self.togglepin(9))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 10",command=lambda : self.togglepin(10))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 11",command=lambda : self.togglepin(11))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 12",command=lambda : self.togglepin(12))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 13",command=lambda : self.togglepin(13))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 14",command=lambda : self.togglepin(14))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 15",command=lambda : self.togglepin(15))
    self.slogan.pack(side=LEFT)
    
    self.slogan = Button(frame,
                             text="Pin 16",command=lambda : self.togglepin(16))
    self.slogan.pack(side=LEFT)
    
  
  def togglepin(self, pin):
    # read the status from the selected pin, invert it and write it back to the pin
    pinstatus = self.bus2.read_pin(pin)
    if (pinstatus == 1):
      pinstatus = 0
    else:
      pinstatus = 1
    self.bus2.write_pin(pin, pinstatus)

root = Tk()
app = App(root)
root.mainloop()