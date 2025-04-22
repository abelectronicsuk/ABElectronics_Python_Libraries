#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi 8-Channel ADC demo

https://www.abelectronics.co.uk/p/69/adc-pi

Requires python smbus to be installed
run with: python demo_readvoltage.py
================================================

Initialise the ADC device using the default addresses and sample rate,
change this value if you have changed the address selection jumpers

Sample rate can be 12, 14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os
import sys


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
        raise ImportError("Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    try:
        # Initialise ADC with default settings

        adc = ADCPi(0x68, 0x69, 18)


        while True:

            # Clear the console
            os.system('clear' if os.name == 'posix' else 'cls')

            # Read and display channel voltages
            print("Channel 1: %02f" % adc.read_voltage(1))
            print("Channel 2: %02f" % adc.read_voltage(2))
            print("Channel 3: %02f" % adc.read_voltage(3))
            print("Channel 4: %02f" % adc.read_voltage(4))
            print("Channel 5: %02f" % adc.read_voltage(5))
            print("Channel 6: %02f" % adc.read_voltage(6))
            print("Channel 7: %02f" % adc.read_voltage(7))
            print("Channel 8: %02f" % adc.read_voltage(8))

            # wait 0.2 seconds before reading again
            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    main()
