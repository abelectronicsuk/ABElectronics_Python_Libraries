#!/usr/bin/env python
"""
================================================
AB Electronics UK: IO Zero 32 | - IO Interrupts Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_iointerrupts.py
================================================

This example shows how to use the interrupt pin on the IO Zero 32 
connected to a GPIO pin on the Raspberry Pi.
Pin 1 on Bus 1 will be set as an input.
GPIO 17 on the Raspberry Pi will set as an input with the internal pull-up resistor enabled.
An interrupt will be enabled on GPIO 17 to call a function when the IN1 pin goes low.
Setting Pin 1 on Bus 1 to high or low will trigger the interrupt and call the interrupt_callback() function.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import signal
import sys
import time
import RPi.GPIO as GPIO

try:
    from IOZero32 import IOZero32
except ImportError:
    print("Failed to import IOZero32 from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from IOZero32 import IOZero32
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

# Create an instance of the IOZero32 class with an I2C address of 0x20    
iobus = IOZero32(0x20)

def signal_handler(sig, frame):
    '''
    Clean-up the GPIO object and exit program
    '''
    GPIO.cleanup()
    sys.exit(0)

def interrupt_callback(channel):
    '''
    This function is called when an interrupt on the GPIO pin occurs
    '''
    x = iobus.read_pin(1)
    print("Interrupt Detected - Pin Value = %d" % x)


def main():
    '''
    Main program function
    '''  

    # Set pin 1 on the IO bus to be an input.
    iobus.set_bus_direction(0x01)

    # Configure the Raspberry Pi GPIO pin 17 as an input with pull-up resistor enabled
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Add an event detect which calls interrupt_callback() when an interrupt occurs
    GPIO.add_event_detect(17, GPIO.FALLING, callback=interrupt_callback, bouncetime=100)

    # Pause the main thread
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()


if __name__ == "__main__":
    main()
    GPIO.cleanup()           # clean up GPIO on normal exit
