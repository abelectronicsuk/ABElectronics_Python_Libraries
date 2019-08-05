#!/usr/bin/env python
"""
================================================
# ABElectronics Expander Pi | ADC Read Demo
#
# Requires python smbus to be installed
# For Python 2 install with: sudo apt-get install python-smbus
# For Python 3 install with: sudo apt-get install python3-smbus
#
# run with: python demo_adcread.py
================================================

this demo reads the voltage from channel 1 on the ADC inputs
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import time
import os
import sys

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


def main():
    '''
    Main program function
    '''
    adc = ExpanderPi.ADC()  # create an instance of the ADC

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the Expander Pi Vref pin.
    adc.set_adc_refvoltage(1.8)

    # clear the console
    os.system('clear')
    while True:
        

         # read the voltage from channels 1 to 8 single ended mode and print
        sys.stdout.write('Pin 1:  %f   \n' % adc.read_adc_voltage(1, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 2:  %f   \n' % adc.read_adc_voltage(2, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 3:  %f   \n' % adc.read_adc_voltage(3, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 4:  %f   \n' % adc.read_adc_voltage(4, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 5:  %f   \n' % adc.read_adc_voltage(5, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 6:  %f   \n' % adc.read_adc_voltage(6, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 7:  %f   \n' % adc.read_adc_voltage(7, 0))
        sys.stdout.flush()
        sys.stdout.write('Pin 8:  %f   \n' % adc.read_adc_voltage(8, 0))
        sys.stdout.flush()
        sys.stdout.write('\033[A\033[A\033[A\033[A\033[A\033[A\033[A\033[A')
        sys.stdout.flush()
        

        time.sleep(0.1)
        

if __name__ == "__main__":
    main()
