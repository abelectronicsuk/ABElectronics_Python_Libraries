#!/usr/bin/python

from ABElectronics_IOPi import IOPI
import time

# ================================================
# ABElectronics IO Pi V2 32-Channel Port Expander
# Version 1.1 Created 30/04/2014
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus 
# run with: sudo python iointerrupts.py
# ================================================

# This example shows how to use the interrupt methods on the IO Pi.  
# The interrupts will be enabled and set so that a voltage applied to pins 1 and 16 will trigger INT A and B respectively.
# using the readInterruptCature or readPort methods will reset the interrupts.



# Initialise the IOPi device using the default addresses and set the output of bank 1 on IC1 to the input of bank 1 on IC2

bus1 = IOPI(0x20)
bus2 = IOPI(0x21)

# Set all pins on bus 2 to be inputs with internal pull-ups disabled.

bus2.setPortPullups(0, 0x00)
bus2.setPortPullups(1, 0x00)
bus2.setPortDirection(0, 0xFF)
bus2.setPortDirection(1, 0xFF)

# Set the interrupt polarity to be active high and mirroring disabled, so pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
bus2.setInterruptPolarity(1)
bus2.mirrorInterrupts(0)

# Set the interrupts default value to trigger when 5V is applied to pins 1 and 16
bus2.setInterruptDefaults(0, 0x01)
bus2.setInterruptDefaults(0, 0x80)

# Set the interrupt type to be 1 for ports A and B so an interrupt is fired when the pin matches the default value
bus2.setInterruptType(0, 1)
bus2.setInterruptType(1, 1)

# Enable interrupts for pins 1 and 16
bus2.setInterruptOnPin(1, 1)
bus2.setInterruptOnPin(16, 1)


while True:

    # read the port value from the last capture for ports 0 and 1.  This will reset the interrupts
    print bus2.readInterruptCature(0)
    print bus2.readInterruptCature(1)
    time.sleep(2)