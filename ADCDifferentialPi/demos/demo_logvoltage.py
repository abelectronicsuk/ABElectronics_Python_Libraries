#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi 8-Channel ADC data-logger demo

https://www.abelectronics.co.uk/p/65/adc-differential-pi

Requires python smbus to be installed
run with: python demo_logvoltage.py
================================================

Use the ADC Differential Pi to log the voltage readings from the 8 ADC channels to a CSV file

Note: to read all 8 channels in under 1 second, you must use 16-bit or lower resolution.

"""

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


def main():
    """
    Main program function
    """

    adc = ADCDifferentialPi(0x68, 0x69, 16) # create an instance of the ADCDifferentialPi class, I2C address 0x68 and 0x69, 16 bit

    interval = 1.0 # sample interval in seconds
    next_run = time.monotonic() # next sample time

    print("Logging...")

    while True:
        next_run += interval

        file = open('adc_log.csv', 'a') # open the log file for appending

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        file.write(timestamp + ",") # write the current time to the log file

        # read from the ADC channels and write to the log file
        file.write("%02f," % adc.read_voltage(1))
        file.write("%02f," % adc.read_voltage(2))
        file.write("%02f," % adc.read_voltage(3))
        file.write("%02f," % adc.read_voltage(4))
        file.write("%02f," % adc.read_voltage(5))
        file.write("%02f," % adc.read_voltage(6))
        file.write("%02f," % adc.read_voltage(7))
        file.write("%02f\n" % adc.read_voltage(8))

        file.close()

        # wait until the next sample time
        sleep_time = next_run - time.monotonic()

        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()

