#!/usr/bin/env python
"""
================================================
AB Electronics UK ADC Pi Soil Moisture Sensor demo

https://www.abelectronics.co.uk/p/69/adc-pi

Requires python smbus to be installed
run with: python demo_soilsensor.py
================================================

This code sample shows how to read the moisture level from a capacitive
soil sensor connected to the ADC Pi.

A tutorial can be found at:
https://www.abelectronics.co.uk/kb/article/1198/adc-pi-with-soil-sensors

"""

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

# Reference voltages based on your calibration
V_DRY = 0.80   # Sensor voltage in dry soil
V_WET = 0.45   # Sensor voltage in wet soil

def moisture_percent(adc_value: float) -> int:
    """
    Convert ADC value to moisture percentage
    :param adc_value: ADC value
    :return: Moisture percentage
    """

    # Calculate the moisture percentage using the formula
    moisture = ((V_DRY - adc_value) / (V_DRY - V_WET)) * 100
    if moisture < 0:
       return 0
    elif moisture > 100:
        return 100
    else:
        return int(moisture)


def main():
    """
    Main program function
    """

    adc = ADCPi(0x68, 0x69, 18)

    # Read and display channel voltages
    voltage = adc.read_voltage(1)
    print("Channel 1: %d%%" % moisture_percent(voltage))


if __name__ == "__main__":
    main()
