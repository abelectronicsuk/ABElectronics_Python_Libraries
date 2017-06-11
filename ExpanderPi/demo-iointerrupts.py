#!/usr/bin/python

from ABE_ExpanderPi import IO
import time

"""
# ================================================
# ABElectronics Expander Pi | - IO Interrupts Demo
# Version 1.0 Created 21/08/2014
# Version 1.1 Updated 11/06/2017 updated to include changes to Expander Pi library
#
# Requires python smbus to be installed with: sudo apt-get install python-smbus
# run with: sudo python demo-iointerrupts.py
# ================================================

# This example shows how to use the interrupt methods on the Expander Pi IO port.
# The interrupts will be enabled and set so that a voltage applied to pins 1 and 16 will trigger INT A and B respectively.
# using the read_interrupt_capture or read_port methods will reset the
# interrupts.


# Initialise the IOPi and create an instance called io.
"""

io = IO()

# Set all pins on the IO bus to be inputs with internal pull-ups disabled.

io.set_port_pullups(0, 0x00)
io.set_port_pullups(1, 0x00)
io.set_port_direction(0, 0xFF)
io.set_port_direction(1, 0xFF)

# Set the interrupt polarity to be active high and mirroring disabled, so
# pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
io.set_interrupt_polarity(1)
io.mirror_interrupts(0)

# Set the interrupts default value to trigger when 5V is applied to pins 1
# and 16
io.set_interrupt_defaults(0, 0x01)
io.set_interrupt_defaults(0, 0x80)

# Set the interrupt type to be 1 for ports A and B so an interrupt is
# fired when the pin matches the default value
io.set_interrupt_type(0, 1)
io.set_interrupt_type(1, 1)

# Enable interrupts for pins 1 and 16
io.set_interrupt_on_pin(1, 1)
io.set_interrupt_on_pin(16, 1)


while True:

    # read the port value from the last capture for ports 0 and 1.  This will
    # reset the interrupts
    print io.read_interrupt_capture(0)
    print io.read_interrupt_capture(1)
    time.sleep(2)
