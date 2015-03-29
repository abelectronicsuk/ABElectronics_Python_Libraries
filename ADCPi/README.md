AB Electronics UK ADC Pi Python Library
=====

Python Library to use with ADC Pi Raspberry Pi expansion board from http://www.abelectronics.co.uk
Install
====

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The ADC Pi library is located in the ADCPi directory

The library requires python-smbus to be installed.
```
sudo apt-get update
sudo apt-get install python-smbus
```
Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ADCPi/
```

The example python files in /ABElectronics_Python_Libraries/ADCPi/ will now run from the terminal.
Functions:
----------
```
read_voltage(channel) 
```
Read the voltage from the selected channel  
**Parameters:** channel - 1 to 8 
**Returns:** number as float between 0 and 5.0

```
read_raw(channel) 
```
Read the raw int value from the selected channel  
**Parameters:** channel - 1 to 8 
**Returns:** number as int

```
set_pga(gain)
```
Set the gain of the PGA on the chip  
**Parameters:** gain -  1, 2, 4, 8  
**Returns:** null

```
setBitRate(rate)
```
Set the sample bit rate of the adc  
**Parameters:** rate -  12, 14, 16, 18  
**Returns:** null  
12 = 12 bit (240SPS max)  
14 = 14 bit (60SPS max)  
16 = 16 bit (15SPS max)  
18 = 18 bit (3.75SPS max)  

```
set_conversion_mode(mode)
```
Set the conversion mode for the adc  
**Parameters:** mode -  0 = One-shot conversion, 1 = Continuous conversion  
**Returns:** null

Usage
====

To use the ADC Pi library in your code you must first import the library:
```
from ABE_ADCPi import ADCPi
```
Now import the helper class
```
from ABE_helpers import ABEHelpers
```
Next you must initialise the adc object and smbus:
```
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCPi(bus, 0x68, 0x69, 18)
```
The first argument is the smbus object folled by the two I2C addresses of the ADC chips. The values shown are the default addresses of the ADC board.

The forth argument is the sample bit rate you want to use on the adc chips. Sample rate can be 12, 14, 16 or 18

You can now read the voltage from channel 1 with:
```
adc.read_voltage(1)
```
