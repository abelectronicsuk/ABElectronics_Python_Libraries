AB Electronics Python Libraries
=====

Python 2.x Libraries to work with Raspberry Pi expansion boards from https://www.abelectronics.co.uk

Python 2.x with smbus

These libraries have been updated to be formatted in PEP8 python formatting on 16 November 2014 and class and function names have been changed to meet the PEP8 styles.  Previous versions of the Python libraries can be found at https://github.com/abelectronicsuk/Archive

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
###ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the ADC DAC Pi https://www.abelectronics.co.uk/p/39/ADC-DAC-Pi-Raspberry-Pi-ADC-and-DAC-expansion-board and the ADC DAC Pi Zero https://www.abelectronics.co.uk/p/74/ADC-DAC-Pi-Zero-Raspberry-Pi-ADC-and-DAC-expansion-board
###ADCPi 
This directory contains ADC Pi Python Library  and read voltage demo to use with the ADC Pi Plus https://www.abelectronics.co.uk/p/56/ADC-Pi-Plus-Raspberry-Pi-Analogue-to-Digital-converter and ADC Pi Zero https://www.abelectronics.co.uk/p/69/ADC-Pi-Zero-Raspberry-Pi-Analogue-to-Digital-converter
###ADCDifferentialPi 
This directory contains ADC Differential Pi Python Library and read voltage demo to use with the ADC Differential Pi https://www.abelectronics.co.uk/p/65/ADC-Differential-Pi-Raspberry-Pi-Analogue-to-Digital-converter
###DeltaSigmaPi
This directory contains Expander Pi Python Library and demos to use with the Delta Sigma Pi https://www.abelectronics.co.uk/kb/article/1041/delta-sigma-pi
###ExpanderPi
This directory contains IO Pi Python Library  and demos to use with the Expander Pi https://www.abelectronics.co.uk/kb/article/1046/expander-pi
###IOPi
This directory contains IO Pi Python Library  and demos to use with the IO Pi Plus https://www.abelectronics.co.uk/p/54/IO-Pi-Plus and IO Pi Zero https://www.abelectronics.co.uk/p/71/IO-Pi-Zero
###RTCPi
This directory contains RTC Pi Python Library and demos to use with the RTC Pi https://www.abelectronics.co.uk/p/15/RTC-Pi , RTC Pi Plus https://www.abelectronics.co.uk/p/52/RTC-Pi-Plus and RTC Pi Zero https://www.abelectronics.co.uk/p/70/RTC-Pi-Zero
###ServoPi
This directory contains ServoPi Python Library  and read voltage demo to use with the ServoPi https://www.abelectronics.co.uk/p/44/Servo-PWM-Pi and Sero Pi Zero https://www.abelectronics.co.uk/p/72/Servo-PWM-Pi-Zero

##Helper class
We have now added ABE_helpers.py class to the libraries which use Python smbus to enable a single bus instance to be used with multiple expansion boards and to avoid smbus conflicts. 
