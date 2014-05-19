AB Electronics UK RTC Pi Python Library
=====

Python Library to use with RTC Pi Raspberry Pi real-time clock board from http://www.abelectronics.co.uk

Install
====

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
The RTC Pi library is located in the ABElectronics_RTCPi directory

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ABElectronics_RTCPi/
```

The example python files in /ABElectronics_Python_Libraries/ABElectronics_RTCPi/ will now run from the terminal.

Functions:
----------

```
setDate(date) 
```
Set the date and time on the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Parameters:** date   
**Returns:** null

```
readDate() 
```
Returns the date from the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Returns:** date


```
enableOutput() 
```
Enable the square-wave output on the SQW pin.  
**Returns:** null

```
disableOutput()
```
Disable the square-wave output on the SQW pin.   
**Returns:** null

```
setFrequency()
```
Set the frequency for the square-wave output on the SQW pin.   
**Parameters:** frequency - options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz   
**Returns:** null

Usage
====

To use the RTC Pi library in your code you must first import the library:
```
from ABElectronics_RTCPi import RTC
```
Next you must initialise the ServoPi object:
```
rtc = RTC()
```
Set the current time in ISO 8601 format:
```
rtc.setDate("2013-04-23T12:32:11")
```
Enable the square-wave output at 8.192KHz on the SQW pin:
```
rtc.setFrequency(3)
rtc.enableOutput()
```
Read the current date and time from the RTC at 1 second intervals:
```
while (True):
  print rtc.readDate()
  time.sleep(1)
```
