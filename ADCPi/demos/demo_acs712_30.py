#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi ACS712 30 Amp current sensor demo

https://www.abelectronics.co.uk/p/69/adc-pi

Requires python smbus to be installed
run with: python demo_acs712_30.py
================================================

Use the ADC Pi to read the voltage from an ACS712 30 Amp current sensor.

"""

import time
import os

try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def calc_current(value):
    """
    Change the 2.5 value to be half of the supply voltage.
    The 0.066 value is the sensitivity of the ACS712 current sensor (mV/A).
    For a 30A sensor this is 0.066mV/A
    For a 20A sensor this is 0.1mV/A
    For a 5A sensor this is 0.185mV/A
    """
    return (value - 2.5) / 0.066


def main():
    """
    Main program function
    """

    adc = ADCPi(0x68, 0x69, 18) # create an instance of the ADC class, I2C address 0x68 and 0x69, 18-bit resolution

    while True:

        # clear the console
        os.system('clear')

        # read from the ADC channels and print to screen
        print("Current on channel 1: %02f" % calc_current(adc.read_voltage(1)))

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)


if __name__ == "__main__":
    main()
