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
import numpy as N

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


def sampleratecheck(adc, rate, samples):
    """
    This function calls read_adc_voltage for a specified
    number of samples and measures how long it takes to complete the task
    """
    # create a counter and arrays to store the sampled voltages for each channel
    counter = 1
    readarray1 = N.zeros(samples)
    readarray2 = N.zeros(samples)
    readarray3 = N.zeros(samples)
    readarray4 = N.zeros(samples)
    readarray5 = N.zeros(samples)
    readarray6 = N.zeros(samples)
    readarray7 = N.zeros(samples)
    readarray8 = N.zeros(samples)

    # set the bit rate of the ADC to the specified rate
    adc.set_bit_rate(rate)

    starttime = datetime.datetime.now()

    while counter < samples:
        # start thread reading channels 1 to 4
        readarray1[counter] = adc.read_voltage(1)
        readarray2[counter] = adc.read_voltage(2)
        readarray3[counter] = adc.read_voltage(3)
        readarray4[counter] = adc.read_voltage(4)
        readarray5[counter] = adc.read_voltage(5)
        readarray6[counter] = adc.read_voltage(6)
        readarray7[counter] = adc.read_voltage(7)
        readarray8[counter] = adc.read_voltage(8)

        counter = counter + 1


    # stop the timer
    endtime = datetime.datetime.now()

    # calculate the samples per second
    totalseconds = (endtime - starttime).total_seconds()
    samplespersecond = samples / totalseconds

    averagevoltage1 = N.average(readarray1)
    averagevoltage2 = N.average(readarray2)
    averagevoltage3 = N.average(readarray3)
    averagevoltage4 = N.average(readarray4)
    averagevoltage5 = N.average(readarray5)
    averagevoltage6 = N.average(readarray6)
    averagevoltage7 = N.average(readarray7)
    averagevoltage8 = N.average(readarray8)

    print("Bit Rate: %i" % (rate))
    print("%.2f samples per seconds" % (samplespersecond * 8))
    print("Average Voltage - Channel 1: %.2f" % (averagevoltage1))
    print("Average Voltage - Channel 2: %.2f" % (averagevoltage2))
    print("Average Voltage - Channel 3: %.2f" % (averagevoltage3))
    print("Average Voltage - Channel 4: %.2f" % (averagevoltage4))
    print("Average Voltage - Channel 5: %.2f" % (averagevoltage5))
    print("Average Voltage - Channel 6: %.2f" % (averagevoltage6))
    print("Average Voltage - Channel 7: %.2f" % (averagevoltage7))
    print("Average Voltage - Channel 8: %.2f" % (averagevoltage8))
    print("---------------------------------------------")
    

def main():
    '''
    Main program function
    '''

    # create an instance of the ADCPi class
    adc = ADCPi(0x68, 0x69, 12)

    adc.set_conversion_mode(1)

    print("Testing ---- This may take some time")

    # 12-bit test - 100 samples
    sampleratecheck(adc, 12, 100)

    # 14-bit test - 100 samples
    sampleratecheck(adc, 14, 100)

    # 16-bit test - 100 samples
    sampleratecheck(adc, 16, 100)

    # 18-bit test - 100 samples
    sampleratecheck(adc, 18, 100)

if __name__ == "__main__":
    main()
