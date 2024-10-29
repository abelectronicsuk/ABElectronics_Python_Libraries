AB Electronics UK I2C Switch Python Library
=====

Python Library to use with [I2C Switch](https://www.abelectronics.co.uk/p/84/i2c-switch "I2C Switch") Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/I2CSwitch/demos  

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

The I2C Switch library is located in the I2CSwitch directory  

To use a specific part of our Python library in your project without installing the entire library, you can simply copy the needed class file into your project's directory. For example, to use the I2C Switch, copy the **I2CSwitch.py** file from the **I2CSwitch** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly utilize the class's functionality in your project.

```
from I2CSwitch import I2CSwitch
```

#### Software Requirements

The library requires I2C to be enabled on the Raspberry Pi and the smbus2 or python-smbus Python library to be installed.  

For Python 2.7:
```
sudo pip install smbus2
```
For Python 3:
```
sudo pip3 install smbus2
```

To configure the I2C bus follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.


# Class: I2CSwitch #

```
I2CSwitch(address, bus)
```
The I2CSwitch class provides control over the I2C Switch outputs on the PCA9546A controller.  Functions include setting and getting the I2C channel and resetting the switch.  

**Parameters:**  
address: Device i2c address. Supported I2C addresses are 0x70 to 0x77. defaults to 0x70  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

Initialise with the I2C address for the I2C Switch. 

```
i2cswitch = I2CSwitch(0x70)
```

Functions:
----------

```
switch_channel(channel) 
```
Switch on the selected channel and switch off all other channels.  
**Parameters:** channel - 1 to 4.  
**Returns:** null  

```
set_channel_state(channel, state) 
```
Set the state for the selected channel.  All other channels remain in their previous state.  
**Parameters:**  
channel - 1 to 4  
state - True or False. True = channel on, False = channel off.  
**Returns:** null  

```
get_channel_state(channel) 
```
Get the state for the selected channel.  
**Parameters:** channel - 1 to 4  
**Returns:** True or False. True = channel on, False = channel off.  

```
reset() 
```
Reset the PCA9546A I2C switch.  Resetting allows the PCA9546A to recover from a situation in which one of the downstream I2C buses is stuck in a low state.  All channels will be set to an off-state.
**Returns:** null  


Usage
====

To use the I2C Switch class in your code you must first import the class:
```
from I2CSwitch import I2CSwitch
```
Next, you must initialise the I2CSwitch object:
```
i2cswitch = I2CSwitch(0x70)
```
Set the I2C switch to channel 2
```
i2cswitch.switch_channel(2)  
```
