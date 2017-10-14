#!/usr/bin/env python
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 3

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: sudo python tutorial3_rpi_interrupts.py
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

def checkbit(byte, bit):
    """
    method for reading the value of a single bit within a byte
    """
    if byte & (1 << bit):
        return 1
    else:
        return 0


def button_pressed(interrupt_pin):
    global bus
    
    """
    this function will be called when GPIO 23 falls low
    """
    # read the interrupt status for ports 0 and 1 and store them in
    # variables porta and portb
    print("Button pressed")
    print(interrupt_pin)
    
    porta = bus.read_interrupt_status(0)
    portb = bus.read_interrupt_status(1)

    # loop through each bit in the porta variable and check if the bit is 1
    # which will indicate a button has been pressed
    for num in range(0, 8):
        if checkbit(porta, num):
            print("Pin " + str(num + 1) + " pressed")

    # repeat for portb
    
    for num in range(0, 8):
        if checkbit(portb, num):
            print("Pin " + str(num + 9) + " pressed")

    # compare the value of porta and portb with the IO Pi port
    # using read_port().  wait until the port changes which will indicate
    # the button has been released.
    # without this while loop the function will keep repeating.

    while ((porta == bus.read_port(0)) and (portb == bus.read_port(1))):
        time.sleep(0.2)

    # reset the interrupts on the bus

    bus.reset_interrupts()


def main():
    """
    Main program function
    """
    global bus
    
    # Create an instance of the IOPi class called bus and 
    # set the I2C address to be 0x20 or Bus 1.

    bus = IOPi(0x20)

    # Set all pins on the bus to be inputs with internal pull-ups enabled.

    bus.set_port_pullups(0, 0xFF)
    bus.set_port_pullups(1, 0xFF)
    bus.set_port_direction(0, 0xFF)
    bus.set_port_direction(1, 0xFF)

    # Inverting the ports will allow a button connected to ground to 
    # register as 1 or on.

    bus.invert_port(0, 0xFF)  # invert port 0 so a button press will register as 1
    bus.invert_port(1, 0xFF)  # invert port 1 so a button press will register as 1

    # Set the interrupt polarity to be active low and mirroring enabled, so
    # INT A and INT B go low when an interrupt is triggered

    bus.set_interrupt_polarity(0)
    bus.mirror_interrupts(1)

    # Set the interrupts default value to 0 so it will trigger when any of 
    # the pins on the bus change to 1

    bus.set_interrupt_defaults(0, 0x00)
    bus.set_interrupt_defaults(1, 0x00)

    # Set the interrupt type to be 0xFF for ports A and B so an interrupt is
    # fired when the pin matches the default value

    bus.set_interrupt_type(0, 0xFF)
    bus.set_interrupt_type(1, 0xFF)

    # Enable interrupts for all pins on the bus

    bus.set_interrupt_on_port(0, 0xFF)
    bus.set_interrupt_on_port(1, 0xFF)

    # reset the interrups on the IO Pi bus

    bus.reset_interrupts()

    # set the GPIO mode to be BCM

    GPIO.setmode(GPIO.BCM)           # Numbers GPIOs by GPIO Order Number

    # Set up GPIO 23 as an input. The pull-up resistor is disabled as the
    # level shifter will act as a pull-up.
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

    # when a falling edge is detected on GPIO pin 23 the function
    # button_pressed will be run

    GPIO.add_event_detect(23, GPIO.FALLING, callback=button_pressed)

    # print out a waiting message and wait for keyboard input before
    # exiting the program

    print("Waiting for button press on IO Pi")

    input("press enter to exit ")


if __name__ == "__main__":
    main()
