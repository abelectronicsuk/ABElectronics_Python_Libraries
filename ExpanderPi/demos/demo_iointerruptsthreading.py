#!/usr/bin/env python
"""
================================================
AB Electronics UK Expander Pi | - IO Interrupts Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iointerruptsthreading.py
================================================

This example shows how to use the interrupt methods with threading
on the Expander Pi IO port.

The interrupts will be enabled and set so that pin 1 will trigger INT A and B.

Internal pull-up resistors will be used so grounding
one of the pins will trigger the interrupt

using the read_interrupt_capture or reset_interrupts methods
will reset the interrupts.

"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import threading

try:
    import ExpanderPi
except ImportError:
    print("Failed to import ExpanderPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        import ExpanderPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def callback_function(bus):
    """
    Call this function from the background_thread function
    This will be called when an interrupt is triggered from
    a state change on pin 1
    """
    print("interrupt triggered")
    if bus.read_pin(1) == 0:
        print("pin 1 was set low")
    else:
        print("pin 1 was set high")


def background_thread(bus):
    """
    Runs in parallel with the main program loop
    """
    while 1:
        # get the interrupt status for INTA
        inta = bus.read_interrupt_status(0)

        # reset the interrupts
        bus.reset_interrupts()

        # check the value of intA to see if an interrupt has occurred
        if inta != 0:
            callback_function(bus)

        # sleep this thread for 0.5 seconds
        time.sleep(0.5)


def main():
    """
    Main program function
    """

    # Create an instance of the IO object

    io_bus = ExpanderPi.IO()

    # Set all pins on the IO bus as inputs with internal pull-ups enabled.

    io_bus.set_port_pullups(0, 0xFF)
    io_bus.set_port_pullups(1, 0xFF)
    io_bus.set_port_direction(0, 0xFF)
    io_bus.set_port_direction(1, 0xFF)

    # invert the ports so pulling a pin to ground will show as 1 instead of 0
    io_bus.invert_port(0, 0xFF)
    io_bus.invert_port(1, 0xFF)

    # Set the interrupt polarity as active high and mirroring enabled, so
    # pin 1 will trigger both INT A and INT B when a pin is grounded
    io_bus.set_interrupt_polarity(1)
    io_bus.mirror_interrupts(1)

    # Set the interrupts default value to 0
    io_bus.set_interrupt_defaults(0, 0x00)
    io_bus.set_interrupt_defaults(1, 0x00)

    # Set the interrupt type as 1 for ports A and B so an interrupt is
    # fired when a state change occurs
    io_bus.set_interrupt_type(0, 0x00)
    io_bus.set_interrupt_type(1, 0x00)

    # Enable interrupts for pin 1
    io_bus.set_interrupt_on_port(0, 0x01)
    io_bus.set_interrupt_on_port(1, 0x00)

    timer = threading.Thread(target=background_thread(io_bus))
    timer.daemon = True  # set thread to daemon ('ok' won't be printed)
    timer.start()

    while 1:
        """
        Do something in the main program loop while the interrupt checking
        is carried out in the background
        """

        # wait 1 second
        time.sleep(1)


if __name__ == "__main__":
    main()
