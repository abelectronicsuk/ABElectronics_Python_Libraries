#!/usr/bin/env python
"""
================================================
AB Electronics UK IO Pi 32-Channel Port Expander - Tutorial 4

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: sudo python tutorial4.py
================================================

This example uses the interrupt pins on the IO Pi to connect to the GPIO port
on the Raspberry Pi via a level shifter.
Connect the INT A pin on the IO Pi to the high side of the level shifter and
GPIO 23 on the Raspberry Pi to the low side.

"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import RPi.GPIO as GPIO

try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

bus = None


def button_pressed(interrupt_pin):
    global bus

    """
    This function will be called when GPIO 23 falls low
    """
    # Read the interrupt capture for port 0 and store it in the variable intval
    interrupt_value = bus.read_interrupt_capture(0)

    # Compare the value of interrupt_value with the IO Pi port 0
    # using read_port(). Wait until the port changes which will indicate
    # the button has been released.
    # Without this while loop the function will keep repeating.

    while interrupt_value == bus.read_port(0):
        time.sleep(0.2)

    # Loop through each bit in the intval variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if interrupt_value & (1 << num):
            print("Pin " + str(num + 1) + " pressed")


def main():
    """
    Main program function
    """
    global bus

    # Create an instance of the IOPi class called bus and
    # set the I2C address to be 0x20 or Bus 1.

    bus = IOPi(0x20)

    # Set port 0 on the bus as inputs with internal pull-ups enabled.

    bus.set_port_pullups(0, 0xFF)
    bus.set_port_direction(0, 0xFF)

    # Inverting the port will allow a button connected to ground to
    # register as 1 or on.

    bus.invert_port(0, 0xFF)

    # Set the interrupt polarity to be active low so Int A and Int B go low
    # when an interrupt is triggered and mirroring disabled, so
    # Int A is mapped to port 0 and Int B is mapped to port 1

    bus.set_interrupt_polarity(0)
    bus.mirror_interrupts(0)

    # Set the interrupts default value to 0, so it will trigger when any of
    # the pins on port 0 change to 1

    bus.set_interrupt_defaults(0, 0x00)

    # Set the interrupt type as 0xFF so an interrupt is
    # fired when the pin matches the default value

    bus.set_interrupt_type(0, 0xFF)

    # Enable interrupts for all pins on port 0

    bus.set_interrupt_on_port(0, 0xFF)

    # Reset the interrupts on the IO Pi bus

    bus.reset_interrupts()

    # Set the Raspberry Pi GPIO mode to be BCM

    GPIO.setmode(GPIO.BCM)

    # Set up GPIO 23 as an input. The pull-up resistor is disabled as the
    # level shifter will act as a pull-up.
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    # When a falling edge is detected on GPIO 23 the function
    # button_pressed will be run

    GPIO.add_event_detect(23, GPIO.FALLING, callback=button_pressed)

    # Print out a message and wait for keyboard input before
    # exiting the program

    input("Press enter to exit ")


if __name__ == "__main__":
    main()
