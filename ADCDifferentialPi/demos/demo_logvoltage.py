#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Differential 8-Channel ADC data-logger demo

Requires python smbus to be installed
run with: python demo_logvoltage.py
================================================

Initialise the ADC device using the default addresses and sample rate, change
this value if you have changed the address selection jumpers

Sample rate can be 12, 14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import datetime


try:
    from ADCDifferentialPi import ADCDifferentialPi
except ImportError:
    print("Failed to import ADCDifferentialPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDifferentialPi import ADCDifferentialPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def write_to_file(text_to_write):
    """
    Save the text to a file
    """
    file = open('adc_log.txt', 'a')
    file.write(str(datetime.datetime.now()) + " " + text_to_write)
    file.close()


def main():
    """
    Main program function
    """

    adc = ADCDifferentialPi(0x68, 0x69, 18)

    while True:

        # read from ADC channels and write to the log file
        write_to_file("Channel 1: %02f\n" % adc.read_voltage(1))
        write_to_file("Channel 2: %02f\n" % adc.read_voltage(2))
        write_to_file("Channel 3: %02f\n" % adc.read_voltage(3))
        write_to_file("Channel 4: %02f\n" % adc.read_voltage(4))
        write_to_file("Channel 5: %02f\n" % adc.read_voltage(5))
        write_to_file("Channel 6: %02f\n" % adc.read_voltage(6))
        write_to_file("Channel 7: %02f\n" % adc.read_voltage(7))
        write_to_file("Channel 8: %02f\n" % adc.read_voltage(8))

        # wait 1 second before reading the pins again
        time.sleep(1)


if __name__ == "__main__":
    main()
