AB Electronics UK IO Zero 32 Python Library
=====

Python Library to use with IO Zero 32 Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/IOZero32/demos  

### Downloading and Installing the library


#### Python 3

To install the library you will need the Python3 build and install packages. To install them run the following command.

```
sudo apt update
sudo apt install python3-build python3-installer git
```

Download the ABElectronics_Python_Libraries to your Raspberry Pi: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library navigate into the ABElectronics_Python_Libraries folder and run:  

```
python3 -m build
sudo python3 -m installer dist/*.whl
```


#### Python 2

If you want to install the library on older versions of Linux using Python 2 you can run the following command.

```
sudo python setup.py install
```

If you have PIP installed you can install the library directly from GitHub with the following command replacing python2.7 with the version of Python on your computer:

```
sudo python2.7 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

#### Using classes without installing the library.

The IO Zero 32 library is located in the IOZero32 directory

To use a specific part of our Python library in your project without installing the entire library, you can simply copy the needed class file into your project's directory. For example, to use the IO Zero 32, copy the **IOZero32.py** file from the **IOZero32** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly utilize the class's functionality in your project.

```
from IOZero32 import IOZero32
```


#### Software Requirements

The library requires I2C to be enabled on the Raspberry Pi and the smbus2 or python-smbus Python library to be installed.  

For Python 2.7:
```
sudo pip install smbus2
```
For Python 3.5:
```
sudo pip3 install smbus2
```

To configure the I2C bus follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

Classes:
----------  
```
IOZero32(address, bus)
```
**Parameters:**  
address: i2c address for the target device. 0x20 to 0x27  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

Functions:
----------
___
```
set_pin_direction(pin, value):
```
Sets the IO direction for an individual pin  
**Parameters:**  
pin: 1 to 16   
value: 1 = input, 0 = output  
**Returns:** null
___
```
get_pin_direction(pin)
```  
Get the IO direction for an individual pin  
**Parameters:**  
pin: pin to read, 1 to 16   
**Returns:** 1 = input, 0 = output  
___
```
set_port_direction(port, value): 
```
Sets the IO direction for the specified IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = input, 0 = output  
**Returns:** null
___
```
get_port_direction(port): 
```
Get the direction from an IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF)  
___
```
set_bus_direction(value): 
```
Sets the IO direction for all pins on the bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF).  For each bit 1 = input, 0 = output  
**Returns:** null
___
```
get_bus_direction()
```
Get the direction for an IO bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = input, 0 = output  
___
```
write_pin(pin, value)
```
Write to an individual pin 1 - 16  
**Parameters:**  
pin: 1 to 16  
value: 1 = logic high, 0 = logic low  
**Returns:** null  
___
```
write_port(port, value)
```
Write to all pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value:  number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  1 = logic high, 0 = logic low    
**Returns:** null  
___
```
write_bus(value)
```
Write to all pins on the selected bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF). For each bit 1 = logic high, 0 = logic low  
**Returns:** null  
___
```
read_pin(pin)
```
Read the value of an individual pin 1 - 16   
**Parameters:**  
pin: 1 to 16  
**Returns:** 0 = logic low, 1 = logic high  
___
```
read_port(port)
```
Read all pins on the selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  0 = logic low, 1 = logic high
___
```
read_bus()
```
Read all pins on the bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF) Each bit in the 16-bit number represents a pin on the port.  0 = logic low, 1 = logic high  
___
```
set_pin_polarity(pin, value)
```
Set the polarity of the selected pin  
**Parameters:**  
pin: 1 to 16  
value: 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null
___
```
get_pin_polarity(pin)
```  
Get the polarity of the selected pin  
**Parameters:**  
pin: pin to read, 1 to 16   
**Returns:** 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
___
```
set_port_polarity(port, value)
```
Set the polarity of the pins on a selected port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16  
value: number between 0 and 255 or 0x00 and 0xFF.  Each bit in the 8-bit number represents a pin on the port.  0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null
___
```
get_port_polarity(port): 
```
Get the polarity for the selected IO port  
**Parameters:**  
port: 0 = pins 1 to 8, 1 = pins 9 to 16   
**Returns:** number between 0 and 255 (0xFF) 
___
```
set_bus_polarity(value)
```
Set the polarity of the pins on the bus  
**Parameters:**  
value: 16-bit number 0 to 65535 (0xFFFF).  For each bit 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null  
___
```
get_bus_polarity()
```
Get the polarity of the pins on the bus  
**Returns:** 16-bit number 0 to 65535 (0xFFFF). For each bit 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
___

Usage
====
To use the IO Zero 32 library in your code you must first import the library:
```
from IOZero32 import IOZero32
```

Next, you must initialise the IOZero32 object with the I2C address of the I/O controller chip.  The default addresses for the IO Zero 32 are 0x20 and 0x21:

```
bus1 = IOZero32(0x20)
```

We will read the inputs 1 to 8 from bus 1 so set port 0 as inputs.  

```
bus1.set_port_direction(0, 0xFF)
```

You can now read pin 1 with:
```
print('Pin 1: ' + str(bus1.read_pin(1)))
```
