AB Electronics UK Expander Pi Python Library
=====

Python Library to use with Expander Pi board from https://www.abelectronics.co.uk

The Expander Pi contains separate classes for the real-time clock, analogue to digital converter, digital to analogue converter and 16 digital I/O pins.  Examples are included to show how each of the classes can be used.

The Expander Pi uses the following devices:  
- Maxim DS1307 Real-time Clock (RTC)  
- Microchip MCP3208 8-channel 12-bit resolution analogue input (ADC)  
- Microchip MCP4822 2 channel 12-bit resolution analogue output (DAC)  
- Microchip MCP23017 16-channel digital I/O controller  

The example python files can be found in /ABElectronics_Python_Libraries/ExpanderPi/demos  


### Downloading and Installing the library

To install the library, you will need the Python3 build and install packages. To install them, run the following command.

```bash
sudo apt update
sudo apt install python3-build python3-installer git
```

Download the ABElectronics_Python_Libraries to your Raspberry Pi: 

```bash
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library, navigate into the ABElectronics_Python_Libraries folder and run:  

```bash
python3 -m build
sudo python3 -m installer dist/*.whl
```

#### Using classes without installing the library.

The Expander Pi library is located in the ExpanderPi directory.  

To use a specific part of our Python library in your project without installing the entire library, you can copy the necessary class file into your project's directory. For example, to use the Expander Pi, copy the **ExpanderPi.py** file from the **ExpanderPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly use the class's functionality in your project.

```python
from ExpanderPi import ExpanderPi
```

#### Software Requirements

The Expander Pi library requires I2C and SPI to be enabled on the Raspberry Pi and the smbus2 or python3-smbus and py-spidev Python libraries to be installed.  

```bash
sudo pip3 install smbus2
```

To configure the SPI bus and install py-spidev follow our [SPI and Python on Raspberry Pi OS](https://www.abelectronics.co.uk/kb/article/2/spi-and-raspbian-linux-on-a-raspberry-pi) tutorial.

To configure the I2C bus, follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

# Class: ADC #

The ADC class controls the functions on the 12-bit 8-channel Analogue to Digital converter.  The Expander Pi comes with an onboard 4.096 voltage reference.  To use an external voltage reference, remove the solder bridge from jumper **J1** and connect the external voltage reference to the Vref pin.

Functions:
----------


```python
read_adc_voltage(channel, mode) 
```   
Read the voltage from the selected channel on the ADC   
**Parameters:** channel - options are: 1 to 8; mode = 0 or 1 where 0 = single-ended and 1 = differential  
**Returns:** voltage

In single-ended mode, the channel number corresponds to the number on the Expander Pi.  
In differential mode, the channel number selects the channels as follows:

| Channel | Mode         | Channel Selection On Expander Pi |
|---------|--------------|----------------------------------|
| 1       | single-ended | 1                                |
| 2       | single-ended | 2                                |
| 3       | single-ended | 3                                |
| 4       | single-ended | 4                                |
| 5       | single-ended | 5                                |
| 6       | single-ended | 6                                |
| 7       | single-ended | 7                                |
| 8       | single-ended | 8                                |
| 1       | differential | CH1 = IN+  CH2 = IN-             |
| 2       | differential | CH1 = IN-  CH2 = IN+             |
| 3       | differential | CH3 = IN+  CH4 = IN-             |
| 4       | differential | CH3 = IN-  CH4 = IN+             |
| 5       | differential | CH5 = IN+  CH6 = IN-             |
| 6       | differential | CH5 = IN-  CH6 = IN+             |
| 7       | differential | CH7 = IN+  CH8 = IN-             |
| 8       | differential | CH7 = IN-  CH8 = IN+             |

___
```python
read_adc_raw(channel, mode) 
```   
Read the raw value from the selected channel on the ADC   
**Parameters:** channel = options are: 1 to 8, mode = 0 or 1 where 0 = single-ended and 1 = differential  
**Returns:** raw 12-bit value (0 to 4096)

In single-ended mode, the channel number corresponds to the number on the Expander Pi.  In differential mode, the channel the number selects the channels as follows:

| Channel | Mode         | Channel Selection On Expander Pi |
|---------|--------------|----------------------------------|
| 1       | single-ended | 1                                |
| 2       | single-ended | 2                                |
| 3       | single-ended | 3                                |
| 4       | single-ended | 4                                |
| 5       | single-ended | 5                                |
| 6       | single-ended | 6                                |
| 7       | single-ended | 7                                |
| 8       | single-ended | 8                                |
| 1       | differential | CH1 = IN+  CH2 = IN-             |
| 2       | differential | CH1 = IN-  CH2 = IN+             |
| 3       | differential | CH3 = IN+  CH4 = IN-             |
| 4       | differential | CH3 = IN-  CH4 = IN+             |
| 5       | differential | CH5 = IN+  CH6 = IN-             |
| 6       | differential | CH5 = IN-  CH6 = IN+             |
| 7       | differential | CH7 = IN+  CH8 = IN-             |
| 8       | differential | CH7 = IN-  CH8 = IN+             |


___
```python
set_adc_refvoltage(voltage) 
```   
Set the reference voltage for the analogue to digital converter.  
By default, the ADC uses an onboard 4.096V voltage reference.  If you choose to use an external voltage reference, you will need to use this method to set the ADC reference voltage to match the supplied reference voltage.
The reference voltage must be less than or equal to the voltage on the Raspberry Pi 5V rail. 

**Parameters:** voltage (use a decimal number)   
**Returns:** null



Usage
====

To use the ADC class in your code, you must first import the library:

```python
from ExpanderPi import ADC
```

Next, you must initialise the ADC object:

```python
adc = ADC()
```

If you are using an external voltage reference, set the voltage using:

```python
adc.set_adc_refvoltage(4.096)
```

Read the voltage from ADC channel 1 in single-ended mode at 1-second intervals:

```python
while True:
  print adc.read_adc_voltage(1,0)
  time.sleep(1)
```

# Class: DAC #

The DAC class controls the 2-channel 12-bit digital-to-analogue converter.  The DAC uses an internal voltage reference and can output a voltage between 0 and 2.048 V.
A gain setting allows you to increase the voltage to between 0 and 4.095 V when the gain is set to 2

Functions:
----------

```python
set_dac_voltage(channel, voltage)
```

Set the voltage for the selected channel on the DAC  
**Parameters:**  
channel - 1 or 2, the voltage can be between 0 and 2.047 volts when the gain is set to 1 or 0 and 4.095 volts when the gain is set to 2  
**Returns:** null 
___

```python
set_dac_raw(channel, value)
```

Set the raw value from the selected channel on the DAC  
**Parameters:**  
channel - 1 or 2, value int between 0 and 4095  
**Returns:** null 

Usage
====

To use the DAC class in your code, you must first import the library:

```python
from ExpanderPi import DAC
```

Next, you must initialise the DAC object with a gain setting of 1 or 2:

```python
dac = DAC(1)
```

Set the channel and voltage for the DAC output.

```python
dac.set_dac_voltage(1, 1.5)
```

# Class: IO #

The IO class controls the 16 digital I/O channels on the Expander Pi.  The MCP23017 chip is split into two 8-bit ports.  Port 0 controls pins 1 to 8, while Port 1 controls pins 9 to 16. 
When writing to or reading from a port, the least significant bit represents the lowest numbered pin on the selected port.  

**Note:** Microchip recommends that pin 8 (GPA7) and pin 16 (GPB7) are used as outputs only.  This change was made for revision D MCP23017 chips manufactured after June 2020. See the [MCP23017 datasheet](https://www.abelectronics.co.uk/docs/pdf/microchip-mcp23017.pdf) for more information.

```python
IO(initialise, bus)
```
**Parameters:**  
initialise (optional): True = direction set as inputs, pullups disabled, ports not inverted. False = device state unaltered., defaults to True  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the I2C bus automatically using the device name.  

Functions:
----------

```python
set_pin_direction(pin, value):
```
Sets the IO direction for an individual pin  
**Parameters:**  
pin: 1 to 16   
value: 1 = input, 0 = output  
**Returns:** null
___
```python
get_pin_direction(pin)
```  
Get the IO direction for an individual pin  
**Parameters:**  
pin: pin to read, 1 to 16   
**Returns:** 1 = input, 0 = output  
___
```python
set_port_direction(port, value): 
```
Sets the IO direction for the specified IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = input, 0 = output  
**Returns:** null
___
```python
get_port_direction(port): 
```
Get the direction from an IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
___
```python
set_bus_direction(value): 
```
Sets the IO direction for all pins on the bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF).  For each bit 1 = input, 0 = output  
**Returns:** null
___
```python
get_bus_direction()
```
Get the direction for an IO bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = input, 0 = output  
___
```python
set_pin_pullup(pin, value)
```
Set the internal 100K pullup resistors for an individual pin  
**Parameters:**  
pin: pin to update, 1 to 16 
value: 1 = enabled, 0 = disabled  
**Returns:** null
___
```python
get_pin_pullup(pin)
```  
Get the internal 100K pullup resistors for an individual pin  
**Parameters:**  
pin: pin to read, 1 to 16  
**Returns:** 1 = enabled, 0 = disabled  
___
```python
set_port_pullups(port, value)
```
Set the internal 100K pullup resistors for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = Enabled, 0 = Disabled  
**Returns:** null  
___
```python
get_port_pullups(port): 
```
Get the internal pullup status for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
___
```python
set_bus_pullups(value)
```
Set internal 100K pullup resistors for an IO bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = enabled, 0 = disabled  
**Returns:** null
___
```python
get_bus_pullups()
```
Get the internal 100K pullup resistors for an IO bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = enabled, 0 = disabled  
___
```python
write_pin(pin, value)
```
Write to an individual pin 1–16  
**Parameters:**  
pin: 1 to 16  
value: 1 = logic high, 0 = logic low  
**Returns:** null  
___
```python
write_port(port, value)
```
Write to all pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = logic high, 0 = logic low    
**Returns:** null  
___
```python
write_bus(value)
```
Write to all pins on the selected bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = logic high, 0 = logic low  
**Returns:** null  
___
```python
read_pin(pin)
```
Read the value of an individual pin 1–16   
**Parameters:**  
pin: 1 to 16  
**Returns:** 0 = logic low, 1 = logic high  
___
```python
read_port(port)
```
Read all pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  0 = logic low, 1 = logic high
___
```python
read_bus()
```
Read all pins on the bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF) Each bit in the 16-bit number represents a pin on the port.  0 = logic low, 1 = logic high  
___
```python
invert_pin(pin, value)
```
Invert the polarity of the selected pin  
**Parameters:**  
pin: 1 to 16  
value: 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null
___
```python
get_pin_polarity(pin)
```  
Get the polarity of the selected pin  
**Parameters:**  
pin: pin to read, 1 to 16   
**Returns:** 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
___
```python
invert_port(port, value)
```
Invert the polarity of the pins on a selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null
___
```python
get_port_polarity(port): 
```
Get the polarity for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF) 
___
```python
invert_bus(value)
```
Invert the polarity of the pins on the bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF).  For each bit 0 = the same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null  
___
```python
get_bus_polarity()
```
Get the polarity of the pins on the bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 0 = the same logic state of the input pin, 1 = inverted logic state of the input pin  
___
```python
mirror_interrupts(value)
```
Sets whether the interrupt pins INT A and INT B are independently connected to each port or internally connected  
**Parameters:**  
value: 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INT A is associated with PortA, and INT B is associated with PortB    
**Returns:** null
___
```python
set_interrupt_polarity(value)
```
Sets the polarity of the INT output pins  
**Parameters:**  
value: 0 = Active Low, 1 = Active High  
**Returns:** null  
___
```python
get_interrupt_polarity()
```
Get the polarity of the INT output pins  
**Returns:** 1 = Active-high.  0 = Active-low.  
___
```python
set_interrupt_type(port, value)
```
Sets the type of interrupt for each pin on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change  
**Returns:** null  
___
```python
get_interrupt_type(port): 
```
Get the type of interrupt for each pin on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
For each bit 1 = interrupt is fired when the pin matches the default value, 0 = interrupt fires on state change  
___
```python
set_interrupt_defaults(port, value)
```
These bits set the compare value for pins configured for interrupt-on-change on the selected port.  
If the associated pin level is the opposite of the register bit, an interrupt occurs.    
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16, 
value: compare value between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  
**Returns:** null  
___
```python
get_interrupt_defaults(port): 
```
Get the interrupt default value for each pin on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
___
```python
set_interrupt_on_pin(pin, value)
```
Enable interrupts for the selected pin  
**Parameters:**  
pin: 1 to 16  
value: 0 = interrupt disabled, 1 = interrupt enabled  
**Returns:** null
___
```python
get_interrupt_on_pin(pin)
```  
Gets whether the interrupt is enabled for the selected pin  
**Parameters:**  
pin: pin to read, 1 to 16   
**Returns:** 1 = enabled, 0 = disabled
___
```python
set_interrupt_on_port(port, value)
```
Enable interrupts for the pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  
**Returns:** null
___
```python
get_interrupt_on_port(port): 
```
Gets whether the interrupts are enabled for the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF).  For each bit 1 = enabled, 0 = disabled  
___
```python
set_interrupt_on_bus(value)
```
Enable interrupts for the pins on the bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF).  For each bit 1 = enabled, 0 = disabled  
**Returns:** null
___
```python
get_interrupt_on_bus()
```
Gets whether the interrupts are enabled for the bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = enabled, 0 = disabled  
___
```python
read_interrupt_status(port)
```
Read the interrupt status for the pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = Enabled, 0 = Disabled
___
```python
read_interrupt_capture(port)
```
Read the value from the selected port at the time of the last interrupt trigger  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = Enabled, 0 = Disabled
___
```python
reset_interrupts()
```
Set the interrupts A and B to 0  
**Parameters:** null  
**Returns:** null

Usage
====

To use the IO Pi library in your code, you must first import the library:

```python
from ExpanderPi import IO
```

Next, you must initialise the IO object:

```python
io = IO()
```

By default, the IO object will be initialised in a reset state with the ports set as inputs, pullup resistors disabled and the pins non-inverted.  If you want to initialise the IO object without updating the port direction or the pullup status, you can add a reset=False parameter.

```python
io = IO(reset=False)
```

We will read inputs 1 to 8 from the I/O bus, so set port 0 as inputs and enable the internal pullup resistors 

```python
io.set_port_direction(0, 0xFF)
io.set_port_pullups(0, 0xFF)
```

You can now read pin 1 with:
```python
print 'Pin 1: ' + str(io.read_pin(1))
```

# Class: RTC #

The RTC class controls the DS1307 real-time clock on the Expander Pi.  You can set and read the date and time from the clock as well as control the pulse output on the RTC pin.  

```python
RTC(bus)
```
**Parameters:**  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

Functions:
----------

```python
set_date(date) 
```

Set the date and time on the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Parameters:** date   
**Returns:** null
___
```python
read_date() 
```

Returns the date from the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Returns:** date

___
```python
enable_output() 
```

Enable the square-wave output on the SQW pin.  
**Returns:** null
___
```python
disable_output()
```

Disable the square-wave output on the SQW pin.   
**Returns:** null
___
```python
set_frequency(frequency)
```

Set the frequency for the square-wave output on the SQW pin.   
**Parameters:** frequency - options are: 1 = 1 Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz   
**Returns:** null
___
```python
write_memory(address, valuearray)
```
Write to the memory on the ds1307. The ds1307 contains 56-Byte, battery-backed RAM with Unlimited Writes  
**Parameters:** address - 0x08 to 0x3F  
valuearray - byte array containing data to be written to memory  
**Returns:** null
___
```python
read_memory(address, length)
```
Read from the memory on the ds1307  
**Parameters:** address - 0x08 to 0x3F 
length - up to 32 bytes.  
The length value cannot exceed the available address space.  
**Returns:** array of bytes

Usage
====

To use the RTC class in your code, you must first import the library:

```python
from ExpanderPi import RTC
```

Next, you must initialise the RTC object:

```python
rtc = RTC()
```

Set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS :

```python
rtc.set_date("2013-04-23T12:32:11")
```

Enable the square-wave output at 8.192KHz on the SQW pin:

```python
rtc.set_frequency(3)
rtc.enable_output()
```

Read the current date and time from the RTC at 1-second intervals:

```python
while True:
  print rtc.read_date()
  time.sleep(1)
```
