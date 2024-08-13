#!/usr/bin/env python

"""
================================================
AB Electronics UK ADC DAC Pi 2-Channel ADC, 2-Channel DAC | ADC Speed Demo

run with: python demo_adcspeed.py
================================================

this demo tests the maximum sample speed for the ADC
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime

import numpy as n

try:
    from ADCDACPi import ADCDACPi
except ImportError:
    print("Failed to import ADCDACPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDACPi import ADCDACPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """

    # create an instance of the ADC DAC Pi with a DAC gain set to 1
    adcdac = ADCDACPi(1)

    # set the reference voltage.  this should be set to the exact voltage
    # measured on the raspberry pi 3.3V rail.
    adcdac.set_adc_refvoltage(3.3)

    counter = 1
    total_samples = 100000

    read_array = n.zeros(total_samples)

    start_time = datetime.datetime.now()
    print("Start: " + str(start_time))

    while counter < total_samples:
        # read the voltage from channel 1 and display on the screen
        read_array[counter] = adcdac.read_adc_voltage(1, 0)

        counter = counter + 1

    end_time = datetime.datetime.now()

    print("End: " + str(end_time))
    total_seconds = (end_time - start_time).total_seconds()

    samples_per_second = total_samples / total_seconds

    print("%.2f samples per second" % samples_per_second)


if __name__ == "__main__":
    main()
