AB Electronics ADC Pi Python Library
=====

Python Library to use with ADC Pi Raspberry Pi expansion board from http://www.abelectronics.co.uk

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The ADC Pi library is located in the ABElectronics_ADCPi directory

The library requires python-smbus to be installed.
```
sudo apt-get update
sudo apt-get install python-smbus
```
Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ABElectronics_ADCPi/
```

The example python files in /ABElectronics_Python_Libraries/ABElectronics_ADCPi/ will now run from the cerminal.

###Methods:

```
readVoltage(channel) 
```
Argument 1 to 8 for the selected ADC Chip

Returns: number as float between 0 and 5

```
readRaw(channel) 
```
Argument 1 to 8 for the selected ADC Chip

Returns: number as int

```
setPGA(gain)
```
Argument gain value, accepted values are 1, 2, 4, 8

Returns: null

```
setBitRate(rate)
```
Argument rate value, accepted values are 12, 14, 16, 18

12 = 12 bit (240SPS max)

14 = 14 bit (60SPS max)

16 = 16 bit (15SPS max)

18 = 18 bit (3.75SPS max)

Returns: null


To use the ADC Pi library in your code you must first import the library:
```
from ABElectronics_ADCPi import ADCPi
```
Next you must initialise the adc object:
```
adc = ADCPi(0x68, 0x69, 18)
```
The first two arguments are the I2C addresses of the ADC chips. The values shown are the default addresses of the ADC board.

The third argement is the sample bit rate you want to use on the adc chips. Sample rate can be 12, 14, 16 or 18

You can now read the voltage from channel 1 with:
```
adc.readVoltage(1)
```
