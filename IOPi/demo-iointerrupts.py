#!/usr/bin/python
"""
================================================
ABElectronics IO Pi V2 32-Channel Port Expander
Version 1.0 Created 30/04/2014
Version 1.1 16/11/2014 updated code and functions to PEP8 format

Requires python smbus to be installed with: sudo apt-get install python-smbus
run with: sudo python demo-iointerrupts.py
================================================

This example shows how to use the interrupt methods on the IO Pi.
The interrupts will be enabled and set so that a voltage applied to
pins 1 and 16 will trigger INT A and B respectively.
using the read_interrupt_capture or read_port methods will
reset the interrupts


Initialise the IOPi device using the default addresses and set the
output of bank 1 on IC1 to the input of bank 1 on IC2
"""
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time

i2c_helper = ABEHelpers()
newbus = i2c_helper.get_smbus()

bus1 = IoPi(newbus, 0x20)
bus2 = IoPi(newbus, 0x21)

# Set all pins on bus 2 to be inputs with internal pull-ups disabled.

bus2.set_port_pullups(0, 0x00)
bus2.set_port_pullups(1, 0x00)
bus2.set_port_direction(0, 0xFF)
bus2.set_port_direction(1, 0xFF)

# Set the interrupt polarity to be active high and mirroring disabled, so
# pins 1 to 8 trigger INT A and pins 9 to 16 trigger INT B
bus2.set_interrupt_polarity(1)
bus2.mirror_interrupts(0)

# Set the interrupts default value to trigger when 5V is applied to pins 1
# and 16
bus2.set_interrupt_defaults(0, 0x01)
bus2.set_interrupt_defaults(0, 0x80)

# Set the interrupt type to be 1 for ports A and B so an interrupt is
# fired when the pin matches the default value
bus2.set_interrupt_type(0, 1)
bus2.set_interrupt_type(1, 1)

# Enable interrupts for pins 1 and 16
bus2.set_interrupt_on_pin(1, 1)
bus2.set_interrupt_on_pin(16, 1)


while True:

    # read the port value from the last capture for ports 0 and 1.  This will
    # reset the interrupts
    print bus2.read_interrupt_capture(0)
    print bus2.read_interrupt_capture(1)
    time.sleep(2)
