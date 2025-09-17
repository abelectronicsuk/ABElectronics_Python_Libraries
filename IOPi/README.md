AB Electronics UK IO Pi Python Library
=====

Python Library to use with IO Pi Plus Raspberry Pi GPIO expansion board from https://www.abelectronics.co.uk/p/54/io-pi-plus

The IO Pi Plus uses the Microchip MCP23017 expander.

For user guides and troubleshooting tips, please visit our knowledge base at https://www.abelectronics.co.uk/kb/article/1132/io-pi-plus  

The example python files can be found in /ABElectronics_Python_Libraries/IOPi/demos  

**Note:** Microchip recommends that pin 8 (GPA7) and pin 16 (GPB7) are used as outputs only.  This change was made for revision D MCP23017 chips manufactured after June 2020. See the [MCP23017 datasheet](https://www.abelectronics.co.uk/docs/pdf/microchip-mcp23017.pdf) for more information.

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

The IO Pi library is located in the IOPi directory  

To use a specific part of our Python library in your project without installing the entire library, you can copy the necessary class file into your project's directory. For example, to use the IO Pi Plus, copy the **IOPi.py** file from the **IOPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly use the class's functionality in your project.

```python
from IOPi import IOPi
```

#### Software Requirements

The library requires I2C to be enabled on the Raspberry Pi and the smbus2 or python3-smbus Python library to be installed.  

```bash
sudo pip3 install smbus2
```

To configure the I2C bus, follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

Classes:
----------  
```python
IOPi(address, initialise, bus)
```
**Parameters:**  
address: i2c address for the target device. 0x20 to 0x27  
initialise (optional): True = direction set as inputs, pull-ups disabled, ports not inverted. False = device state unaltered., defaults to True  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

Functions:
----------
___
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
Set the internal 100K pull-up resistors for an individual pin  
**Parameters:**  
pin: pin to update, 1 to 16 
value: 1 = enabled, 0 = disabled  
**Returns:** null
___
```python
get_pin_pullup(pin)
```  
Get the internal 100K pull-up resistors for an individual pin  
**Parameters:**  
pin: pin to read, 1 to 16  
**Returns:** 1 = enabled, 0 = disabled  
___
```python
set_port_pullups(port, value)
```
Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = Enabled, 0 = Disabled  
**Returns:** null  
___
```python
get_port_pullups(port): 
```
Get the internal pull-up status for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
___
```python
set_bus_pullups(value)
```
Set internal 100K pull-up resistors for an IO bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = enabled, 0 = disabled  
**Returns:** null
___
```python
get_bus_pullups()
```
Get the internal 100K pull-up resistors for an IO bus  
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
If the associated pin level is the opposite to the register bit, an interrupt occurs.    
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
from IOPi import IOPi
```

Next, you must initialise the IO object with the I2C address of the I/O controller chip.  The default addresses for the IO Pi are 0x20 and 0x21:

```python
bus1 = IOPI(0x20)
```

We will read inputs 1 to 8 from bus 2, so set port 0 as inputs and enable the internal pull-up resistors 

```python
bus1.set_port_direction(0, 0xFF)
bus1.set_port_pullups(0, 0xFF)
```

You can now read pin 1 with:
```python
print('Pin 1: ' + str(bus1.read_pin(1)))
```
