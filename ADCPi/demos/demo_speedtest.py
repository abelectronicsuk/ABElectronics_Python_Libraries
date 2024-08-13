#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi 8-Channel ADC speed test demo

Requires python3 smbus to be installed
run with: python3 demo_speedtest.py
================================================

Initialise the ADC device using the default addresses and test the
samples per second at each bit rate

"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import datetime
import numpy as n

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


def sample_rate_check(adc, rate, samples):
    """
    This function calls read_adc_voltage for a specified
    number of samples and measures how long it takes to complete the task
    """
    # create a counter and arrays to store the sampled voltages for each channel
    counter = 1
    read_array1 = n.zeros(samples)
    read_array2 = n.zeros(samples)
    read_array3 = n.zeros(samples)
    read_array4 = n.zeros(samples)
    read_array5 = n.zeros(samples)
    read_array6 = n.zeros(samples)
    read_array7 = n.zeros(samples)
    read_array8 = n.zeros(samples)

    # set the bit rate of the ADC to the specified rate
    adc.set_bit_rate(rate)

    start_time = datetime.datetime.now()

    while counter < samples:
        # start thread reading channels 1 to 4
        read_array1[counter] = adc.read_voltage(1)
        read_array2[counter] = adc.read_voltage(2)
        read_array3[counter] = adc.read_voltage(3)
        read_array4[counter] = adc.read_voltage(4)
        read_array5[counter] = adc.read_voltage(5)
        read_array6[counter] = adc.read_voltage(6)
        read_array7[counter] = adc.read_voltage(7)
        read_array8[counter] = adc.read_voltage(8)

        counter = counter + 1

    # stop the timer
    end_time = datetime.datetime.now()

    # calculate the samples per second
    total_seconds = (end_time - start_time).total_seconds()
    samples_per_second = samples / total_seconds

    average_voltage1 = n.average(read_array1)
    average_voltage2 = n.average(read_array2)
    average_voltage3 = n.average(read_array3)
    average_voltage4 = n.average(read_array4)
    average_voltage5 = n.average(read_array5)
    average_voltage6 = n.average(read_array6)
    average_voltage7 = n.average(read_array7)
    average_voltage8 = n.average(read_array8)

    print("Bit Rate: %i" % rate)
    print("%.2f samples per seconds" % (samples_per_second * 8))
    print("Average Voltage - Channel 1: %.2f" % average_voltage1)
    print("Average Voltage - Channel 2: %.2f" % average_voltage2)
    print("Average Voltage - Channel 3: %.2f" % average_voltage3)
    print("Average Voltage - Channel 4: %.2f" % average_voltage4)
    print("Average Voltage - Channel 5: %.2f" % average_voltage5)
    print("Average Voltage - Channel 6: %.2f" % average_voltage6)
    print("Average Voltage - Channel 7: %.2f" % average_voltage7)
    print("Average Voltage - Channel 8: %.2f" % average_voltage8)
    print("---------------------------------------------")
    

def main():
    """
    Main program function
    """

    # create an instance of the ADCPi class
    adc = ADCPi(0x68, 0x69, 12)

    adc.set_conversion_mode(1)

    print("Testing ---- This may take some time")

    # 12-bit test - 100 samples
    sample_rate_check(adc, 12, 100)

    # 14-bit test - 100 samples
    sample_rate_check(adc, 14, 100)

    # 16-bit test - 100 samples
    sample_rate_check(adc, 16, 100)

    # 18-bit test - 100 samples
    sample_rate_check(adc, 18, 100)


if __name__ == "__main__":
    main()
