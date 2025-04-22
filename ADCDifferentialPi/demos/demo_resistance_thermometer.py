#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Differential Pi 8-Channel ADC read Resistance thermometer
using a Wheatstone bridge.

https://www.abelectronics.co.uk/p/65/adc-differential-pi

This demo uses a Semitec NTC (Negative Temperature Coefficient) Thermistors
10kOhm 1%, Manufacturer Part No: 103AT-11

Purchased from Mouser Electronics, Part No: 954-103AT-11

The circuit is connected to the + and - inputs on channel 7 on the
ADC Differential Pi. This can also be used on the Delta Sigma Pi

The Wheatstone bridge comprises three 10K resistors and the
Resistance thermometer


Requires python smbus to be installed
run with: python demo_resistance_thermometer.py
================================================

Initialise the ADC device using the default addresses and 18-bit sample rate,
change this value if you have changed the address selection jumpers
Bit-rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import math
import time
import os

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

# the resistor values for the Wheatstone bridge are:
RESISTOR1 = 10000.0
RESISTOR2 = 10000.0
RESISTOR3 = 10000.0
# Input voltage
VOLT_IN = 3.3
# Resistance thermometer values from the datasheet
B_RESISTANCE = 3435.0
T25RESISTANCE = 10000.0
T0 = 273.15
T25 = T0 + 25.0


def calc_resistance(voltage):
    """
    Calculate the Resistance
    """
    return (RESISTOR2 * RESISTOR3 + RESISTOR3 * (RESISTOR1+RESISTOR2) * voltage /
            VOLT_IN) / (RESISTOR1 - (RESISTOR1 + RESISTOR2) * voltage / VOLT_IN)


def calc_temperature(resistance):
    """
    Calculate the temperature
    """
    return 1 / ((math.log(resistance / T25RESISTANCE) / B_RESISTANCE) +
                (1 / T25)) - T0


def main():
    """
    Main program function
    """

    adc = ADCDifferentialPi(0x68, 0x69, 18)

    # loop forever reading the values and printing them to screen
    while True:
        # read from ADC channels and print to screen

        bridge_voltage = adc.read_voltage(1)
        therm_resistance = calc_resistance(bridge_voltage)
        temperature = calc_temperature(therm_resistance)

        # clear the console
        os.system('clear')

        # print values to screen
        print("Bridge Voltage: %02f volts" % bridge_voltage)
        print("Resistance: %d ohms" % therm_resistance)
        print("Temperature: %.2fC" % temperature)

        # wait 0.5 seconds before reading the pins again
        time.sleep(0.5)


if __name__ == "__main__":
    main()
