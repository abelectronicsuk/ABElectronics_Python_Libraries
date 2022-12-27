#!/usr/bin/env python

from distutils.core import setup

setup(
    name='abelectronics',
    version='2.4.5',
    description='AB Electronics UK Python Libraries',
    author='AB Electronics UK',
    author_email='sales@abelectronics.co.uk',
    license='MIT',
    url='https://github.com/abelectronicsuk/ABElectronics_Python_Libraries',
    packages=['ADCDACPi', 'ADCDifferentialPi', 'ADCPi', 'ExpanderPi', 'I2CSwitch', 'IOPi', 'IOZero32','RTCPi', 'ServoPi'],
)
