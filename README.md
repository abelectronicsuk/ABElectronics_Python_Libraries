AB Electronics Python Libraries
=====

Python 2.x Libraries to work with Raspberry Pi expansion boards from http://www.abelectronics.co.uk

Python 2.x with smbus

These libraries have been updated to be formatted in PEP8 python formatting on 16 November 2014 and class and function names have been changed to meet the PEP8 styles.  Previous versions of the Python libraries can be found at ```https://github.com/abelectronicsuk/Archive```

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
###ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the ADC DAC Pi from  https://www.abelectronics.co.uk/products/3/Raspberry-Pi/39/ADC-DAC-Pi-Raspberry-Pi-ADC-and-DAC-expansion-board
###ADCPi 
This directory contains ADC Pi Python Library  and read voltage demo to use with the ADC Pi v2 from  http://www.abelectronics.co.uk/products/3/Raspberry-Pi/17/ADC-Pi-V2---Raspberry-Pi-Analogue-to-Digital-converter
###DeltaSigmaPi
This directory contains Expander Pi Python Library and demos to use with the Expander Pi from http://www.abelectronics.co.uk/products/3/Raspberry-Pi/14/Delta-Sigma-Pi-18-bit-Analogue-to-Digital-converter
###ExpanderPi
This directory contains IO Pi Python Library  and demos to use with the IO Pi from https://www.abelectronics.co.uk/products/3/Raspberry-Pi/50/Expander-Pi
###IOPi
This directory contains IO Pi Python Library  and demos to use with the IO Pi from http://www.abelectronics.co.uk/products/3/Raspberry-Pi/18/IO-Pi-32-Channel-Port-Expander-for-the-Raspberry-Pi
###RTCPi
This directory contains RTC Pi Python Library and demos to use with the RTC Pi from https://www.abelectronics.co.uk/products/3/Raspberry-Pi/15/RTC-Pi
###ServoPi
This directory contains ServoPi Python Library  and read voltage demo to use with the ServoPi from http://www.abelectronics.co.uk/products/3/Raspberry-Pi/44/Servo-Pi---PWM-Controller

##Helper class
We have now added ABE_helpers.py class to the libraries which use Puthon smbus to enable a single bus instance to be used with multiple expansion boards and to avoid smbus conflicts. 
