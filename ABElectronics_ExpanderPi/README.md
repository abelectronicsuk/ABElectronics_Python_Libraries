AB Electronics UK Expander Pi Python Library
=====

Python Library to use with Expander Pi board from http://www.abelectronics.co.uk

The Expander Pi contains separate classes for the real-time clock, analogue to digital converter, digital to analogue converter and the digital I/O pins.  Examples are included to show how each of the classes can be used.

Install
====

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
The Expander Pi library is located in the ABElectronics_ExpanderPi directory

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ABElectronics_ExpanderPi/
```

The example python files in /ABElectronics_Python_Libraries/ABElectronics_ExpanderPi/ will now run from the terminal.

# Class: ADC #

The ADC class controls the functions on the 12 bit 8 channel Analogue to Digital converter.  The Expander Pi comes with an on board  4.096 voltage reference.  To use an external voltage reference remover the solder bridge from jumper J1 and connect the external voltage reference to the Vref pin.




Functions:
----------

```
readADCvoltage(channel) 
```   
Read the voltage from the selected channel on the ADC   
**Parameters:** channel = options are: 1 to 8   
**Returns:** voltage

```
readADCraw(channel) 
```   
Read the raw value from the selected channel on the ADC   
**Parameters:** channel = options are: 1 to 8   
**Returns:** raw 12 bit value (0 to 4096)


```
setADCrefvoltage(voltage) 
```   
set the reference voltage for the analogue to digital converter.  
By default the ADC uses an on-board 4.096V voltage reference.  If you choose to use an external voltage reference you will need to use this method to set the ADC reference voltage to match the supplied reference voltage.
The reference voltage must be less than or equal to the voltage on the Raspberry Pi 5V rail. 

**Parameters:** voltage (use a decimal number)   
**Returns:** null



Usage
====

To use the ADC class in your code you must first import the library:

```
from ABElectronics_ExpanderPi import ADC
```

Next you must initialise the ADC object:

```
adc = ADC()
```

If you are using an external voltage reference set the voltage using:

```
adc.setADCrefvoltage(4.096)
```

Read the voltage from the ADC channel 1 at 1 second intervals:

```
while (True):
  print adc.readADCvoltage(1)
  time.sleep(1)
```

# Class: DAC #

The DAC class controls the 2 channel 12 bit digital to analogue converter.  The DAC uses an internal voltage reference and can output a voltage between 0 and 2.048V.

Functions:
----------

```
setDACvoltage(channel, voltage)
```

Set the voltage for the selected channel on the DAC  
**Parameters:** channel - 1 or 2,  voltage can be between 0 and 2.047 volts  
**Returns:** null 

```
setDACraw(channel, value)
```

Set the raw value from the selected channel on the DAC  
**Parameters:** channel - 1 or 2,value int between 0 and 4095  
**Returns:** null 
Usage
====

To use the DAC class in your code you must first import the library:

```
from ABElectronics_ExpanderPi import DAC
```

Next you must initialise the DAC object:

```
dac = DAC()
```

Set the channel and voltage for the DAC output.

```
dac.setDACvoltage(1, 1.5)
```

# Class: IO #

The IO class controls the 16 digital I/O channels on the Expander Pi.  The MCP23017 chip is split into two 8-bit ports.  Port 0 controls pins 1 to 8 while Port 1 controls pins 9 to 16. 
When writing to or reading from a port the least significant bit represents the lowest numbered pin on the selected port.

Functions:
----------

```
setPinDirection(pin, direction):
```

Sets the IO direction for an individual pin  
**Parameters:** pin - 1 to 16, direction - 1 = input, 0 = output  
**Returns:** null

```
setPortDirection(port, direction): 
```

Sets the IO direction for the specified IO port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, direction - 1 = input, 0 = output  
**Returns:** null

```
setPortPullups(self, port, value)
```

Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:** port - 1 to 16, value: 1 = Enabled, 0 = Disabled  
**Returns:** null

```
writePin(pin, value)
```

Write to an individual pin 1 - 16  
**Parameters:** pin - 1 to 16, value - 1 = Enabled, 0 = Disabled
**Returns:** null

```
writePort(self, port, value)
```

Write to all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, value -  number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
readPin(pin)
```

Read the value of an individual pin 1 - 16   
**Parameters:** pin: 1 to 16  
**Returns:** 0 = logic level low, 1 = logic level high

```
readPort(port)
```

Read all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF

```
invertPort(port, polarity)
```

Invert the polarity of the pins on a selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 8 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null

```
invertPin(pin, polarity)
```

Invert the polarity of the selected pin  
**Parameters:** pin - 1 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
**Returns:** null

```
mirrorInterrupts(value)
```

Mirror Interrupts  
**Parameters:** value - 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INTA is associated with PortA and INTB is associated with PortB  
**Returns:** null

```
setInterruptType(port, value)
```

Sets the type of interrupt for each pin on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: 1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change  
**Returns:** null

```
setInterruptDefaults(port, value)
```

These bits set the compare value for pins configured for interrupt-on-change on the selected port.  
If the associated pin level is the opposite from the register bit, an interrupt occurs.    
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: compare value  
**Returns:** null

```
setInterruptOnPort(port, value)
```

Enable interrupts for the pins on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16, value: number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
setInterruptOnPin(pin, value)
```

Enable interrupts for the selected pin  
**Parameters:** pin - 1 to 16, value - 0 = interrupt disabled, 1 = interrupt enabled  
**Returns:** null

```
readInterruptStatus(port)
```

Enable interrupts for the selected pin  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** status

```
readInterruptCature(port)
```

Read the value from the selected port at the time of the last interrupt trigger  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 8 to 16  
**Returns:** status

```
resetInterrupts()
```

Set the interrupts A and B to 0  
**Parameters:** null  
**Returns:** null

Usage
====

To use the IO Pi library in your code you must first import the library:

```
from ABElectronics_ExpanderPi import IO
```

Next you must initialise the IO object:

```
io = IO()
```

We will read the inputs 1 to 8 from the I/O bus so set port 0 to be inputs and enable the internal pull-up resistors 

```
io.setPortDirection(0, 0xFF)
io.setPortPullups(0, 0xFF)
```

You can now read the pin 1 with:
```
print 'Pin 1: ' + str(io.readPin(1))
```

# Class: RTC #

The RTC class controls the DS1307 real-time clock on the Expander Pi.  You can set and read the date and time from the clock as well as controlling the pulse output on the RTC pin.

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

To use the RTC class in your code you must first import the library:

```
from ABElectronics_ExpanderPi import RTC
```

Next you must initialise the RTC object:

```
rtc = RTC()
```

Set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS :

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
