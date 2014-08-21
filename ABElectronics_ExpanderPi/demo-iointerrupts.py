#!/usr/bin/python

from ABElectronics_ExpanderPi import IO
import time

# ================================================
# ABElectronics Expander Pi | - IO Interrupts Demo
# Version 1.0 Created 21/08/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python demo-iointerrupts.py
# ================================================

# This example shows how to use the interrupt methods on the Expander Pi IO port.  
# The interrupts will be enabled and set so that a voltage applied to pins 1 and 16 will trigger INT A and B respectively.
# using the readInterruptCature or readPort methods will reset the interrupts.



# Initialise the IOPi and create an instance called io.

io = IO()

# Set all pins on the IO bus to be inputs with internal pull-ups disabled.

io.setPortPullups(0, 0x00)
io.setPortPullups(1, 0x00)
io.setPortDirection(0, 0xFF)
io.setPortDirection(1, 0xFF)

# Set the interrupt polarity to be active high and mirroring disabled, so pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
io.setInterruptPolarity(1)
io.mirrorInterrupts(0)

# Set the interrupts default value to trigger when 5V is applied to pins 1 and 16
io.setInterruptDefaults(0, 0x01)
io.setInterruptDefaults(0, 0x80)

# Set the interrupt type to be 1 for ports A and B so an interrupt is fired when the pin matches the default value
io.setInterruptType(0, 1)
io.setInterruptType(1, 1)

# Enable interrupts for pins 1 and 16
io.setInterruptOnPin(1, 1)
io.setInterruptOnPin(16, 1)


while True:

    # read the port value from the last capture for ports 0 and 1.  This will reset the interrupts
    print io.readInterruptCature(0)
    print io.readInterruptCature(1)
    time.sleep(2)