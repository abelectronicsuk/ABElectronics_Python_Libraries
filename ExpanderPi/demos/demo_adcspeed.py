#!/usr/bin/env python

"""
================================================
# AB Electronics UK Expander Pi | ADC Speed Demo
#
# Requires python smbus to be installed
# For Python 2 install with: sudo apt-get install python-smbus
# For Python 3 install with: sudo apt-get install python3-smbus
#
# run with: python demo_adcspeed.py
================================================

This demo tests the maximum sample speed for the ADC

"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import numpy as n

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
    """
    Main program function
    """

    adc = ExpanderPi.ADC()  # create an instance of the ADC

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the Expander Pi Vref pin.
    adc.set_adc_refvoltage(4.096)

    counter = 1
    total_samples = 100000

    read_array = n.zeros(total_samples)

    start_time = datetime.datetime.now()
    print("Start: " + str(start_time))

    while counter < total_samples:
        # read the voltage from channel 1 and display on the screen
        read_array[counter] = adc.read_adc_voltage(1, 0)

        counter = counter + 1

    end_time = datetime.datetime.now()

    print("End: " + str(end_time))
    total_seconds = (end_time - start_time).total_seconds()

    samples_per_second = total_samples / total_seconds

    print("%.2f samples per second" % samples_per_second)


if __name__ == "__main__":
    main()
