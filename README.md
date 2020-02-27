AB Electronics Python Libraries
=====

Python Libraries to work with Raspberry Pi expansion boards from https://www.abelectronics.co.uk

#### 07-07-2017 Major Update - Now compatible with Python 2 and 3

Version 2.0.0 of the Python library has introduced several changes to the structure of the classes and demo files.  The major changes are listed below.  Please read CHANGELOG.md for a complete list of changes.

* Files renamed: removed ABE_ from all names.  
ABE_ADCDACPi > ADCDACPi  
ABE_ADCDifferentialPi > ADCDifferentialPi  
ABE_ADCPi > ADCPi  
ABE_ExpanderPi > ExpanderPi  
ABE_IOPi > IOPi  
ABE_RTCPi > RTCPi  
ABE_ServoPi >  ServoPi

* All classes and demo files are now compatible with Python 2 and 3.  The ABElectronics_Python3_Libraries will no longer be updated so please use this version instead for your Python 3 projects.
* Moved all demo files into demo sub-folders for each class
* The ABE_Helper class has been integrated into the board classes and does not need to be imported separately.
* Added a setup.py into the root for installing the this library into the main Python library directory.

Previous versions of the Python libraries can be found at https://github.com/abelectronicsuk/Archive

### Downloading and Installing the library

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library navigate into the ABElectronics_Python_Libraries folder and run:  

For Python 2.7:
```
sudo python setup.py install
```
For Python 3.5:
```
sudo python3 setup.py install
```

If you have PIP installed you can install the library directly from github with the following command:

For Python 2.7:
```
sudo python2.7 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

For Python 3.5:
```
sudo python3.5 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

### ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the ADC DAC Pi  
https://www.abelectronics.co.uk/p/74/adc-dac-pi-zero-raspberry-pi-adc-and-dac-expansion-board
### ADCPi 
This directory contains ADC Pi Python Library  and read voltage demo to use with the ADC Pi   
https://www.abelectronics.co.uk/p/69/adc-pi-raspberry-pi-analogue-to-digital-converter
### ADCDifferentialPi 
This directory contains ADC Differential Pi Python Library and read voltage demo to use with the ADC Differential Pi.  
https://www.abelectronics.co.uk/p/65/adc-differential-pi-raspberry-pi-analogue-to-digital-converter
This library is also compatible with the Delta-Sigma Pi.  
https://www.abelectronics.co.uk/kb/article/1041/delta-sigma-pi
### ExpanderPi
This directory contains IO Pi Python Library  and demos to use with the Expander Pi https://www.abelectronics.co.uk/p/50/expander-pi
### I2C Switch  
This directory contains the I2C Switch Python library and demo to use with the 4 channel [I2C switch](https://www.abelectronics.co.uk/p/84/i2c-switch "I2C Switch")  

### IOPi
This directory contains IO Pi Python Library  and demos to use with the IO Pi Plus https://www.abelectronics.co.uk/p/54/io-pi-plus and IO Pi Zero https://www.abelectronics.co.uk/p/71/io-pi-zero
### RTCPi
This directory contains RTC Pi Python Library and demos to use with the RTC Pi https://www.abelectronics.co.uk/p/70/rtc-pi 
### ServoPi
This directory contains ServoPi Python Library  and read voltage demo to use with the ServoPi https://www.abelectronics.co.uk/p/72/servo-pwm-pi
