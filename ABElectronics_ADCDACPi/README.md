AB Electronics ADCDAC Pi Python Library
=====

Python Library to use with ADCDAC Pi Raspberry Pi expansion board from http://www.abelectronics.co.uk

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

The ADCDAC Pi library is located in the ABElectronics_ADCDACPi directory

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ABElectronics_ADCDACPi/
```

The example python files in /ABElectronics_Python_Libraries/ABElectronics_ADCPi/ will now run from the terminal.

###Methods:

```
readADCvoltage(channel) 
```
Read the voltage from the selected channel on the ADC

Argument: 1 or 2

Returns: number as float between 0 and 2.048

```
readADCraw(channel) 
```
Read the raw value from the selected channel on the ADC

Argument: 1 or 2

Returns: number as int

```
setADCrefvoltage(voltage)
```
Set the reference voltage for the analogue to digital converter.  
The ADC uses the raspberry pi 3.3V power as a voltage reference so using this method to set the reference to match the exact output voltage from the 3.3V regulator will increase the accuracy of the ADC readings.

Argument: float between 0.0 and 7.0

Returns: null

```
setDACvoltage(channel, voltage)
```
Set the voltage for the selected channel on the DAC

Argument: voltage can be between 0 and 2.047 volts

channel: 1 or 2

Returns: null

```
setDACraw(channel, value)
```
Set the raw value from the selected channel on the DAC

Argument: value between 0 and 4095

channel: 1 or 2

Returns: null

To use the ADCDAC Pi library in your code you must first import the library:
```
from ABElectronics_ADCDACPi import ADCDACPi
```
Next you must initialise the adcdac object:
```
adcdac = ADCDACPi()
```
Set the reference voltage.
```
adcdac.setADCrefvoltage(3.3)
```
Read the voltage from channel 2 and display on the screen
```
print adcdac.readADCvoltage(2)
```
