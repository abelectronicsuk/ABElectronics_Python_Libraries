#!/usr/bin/python

from ABE_ExpanderPi import IO
import time
import threading
import os

"""
# ================================================
# ABElectronics Expander Pi | - IO Interrupts Demo
# Version 1.0 Created 26/06/2015
# Version 1.1 Updated 11/06/2017 updated to include changes to Expander Pi library
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus
#
# run with: sudo python demo-iointerruptsthreading.py
# ================================================

# This example shows how to use the interrupt methods with threading on the Expander Pi IO port.
# The interrupts will be enabled and set so that pin 1 will trigger INT A and B.
# Internal pull-up resistors will be used so grounding one of the pins will trigger the interrupt
# using the read_interrupt_capture or reset_interrupts methods will reset the interrupts.


# Initialise the IOPi and create an instance called io.
"""

def callback_function():
    """
    Function we want to call from the background_thread function
    This function will be called when an interrupt is triggered from a state change on pin 1
    """
    print "interrupt triggered" 
    if (io.read_pin(1) == 0):
       print "pin 1 was set low"          
    else:
       print "pin 1 was set high"  

def background_thread():
    """
    Function we want to run in parallel with the main program loop
    """
    while(1):       
        # get the interrupt status for INTA
        intA = io.read_interrupt_status(0)
        
        # reset the interrupts
        io.reset_interrupts()

        # check the value of intA to see if an interrupt has occurred
        if (intA != 0):
            callback_function()
            
        # sleep this thread for 0.5 seconds
        time.sleep(0.5)

    
# Create an instance of the IO object

io = IO()

# Set all pins on the IO bus to be inputs with internal pull-ups enabled.

io.set_port_pullups(0, 0xFF)
io.set_port_pullups(1, 0xFF)
io.set_port_direction(0, 0xFF)
io.set_port_direction(1, 0xFF)

# invert the ports so pulling a pin to ground will show as 1 instead of 0
io.invert_port(0,0xFF)
io.invert_port(1,0xFF)

# Set the interrupt polarity to be active high and mirroring enabled, so
# pin 1 will trigger both INT A and INT B when a pin is grounded
io.set_interrupt_polarity(1)
io.mirror_interrupts(1)

# Set the interrupts default value to 0
io.set_interrupt_defaults(0, 0x00)
io.set_interrupt_defaults(1, 0x00)

# Set the interrupt type to be 1 for ports A and B so an interrupt is
# fired when a state change occurs
io.set_interrupt_type(0, 0x00)
io.set_interrupt_type(1, 0x00)

# Enable interrupts for pin 1
io.set_interrupt_on_port(0, 0x01)
io.set_interrupt_on_port(1, 0x00)


t=threading.Thread(target=background_thread)
t.daemon = True  # set thread to daemon ('ok' won't be printed in this case)
t.start()


while 1:
    """
        Do something in the main program loop while the interrupt checking is carried out in the background    
    """
    
    # wait 1 seconds
    time.sleep(1)
