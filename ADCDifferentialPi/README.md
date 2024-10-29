AB Electronics UK ADC Differential Pi Python Library
=====

Python Library to use with ADC Differential Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/ADCDifferentialPi/demos  

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

The ADC Differential Pi library is located in the ADCDifferentialPi directory  

To use a specific part of our Python library in your project without installing the entire library, you can simply copy the needed class file into your project's directory. For example, to use the ADC Pi, copy the **ADCDifferentialPi.py** file from the **ADCDifferentialPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly utilize the class's functionality in your project.

```
from ADCDifferentialPi import ADCDifferentialPi
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

Classes:
----------  
```
ADCDifferentialPi(address, address2, rate, bus)
```
**Parameters:**  
address: I2C address for channels 1 to 4, defaults to 0x68  
address2: I2C address for channels 5 to 8, defaults to 0x69  
rate: bit rate, values can be 12, 14, 16 or 18. Defaults to 18  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

Functions:
----------
```
read_voltage(channel) 
```
Read the voltage from the selected channel  
**Parameters:** channel - 1 to 8 
**Returns:** number as a float between -2.048 and +2.048

```
read_raw(channel) 
```
Read the raw int value from the selected channel  
**Parameters:** channel - 1 to 8 
**Returns:** number as an int

```
set_pga(gain)
```
Set the gain of the PGA on the chip  
**Parameters:** gain -  1, 2, 4, 8  
**Returns:** null

```
set_bit_rate(rate)
```
Set the sample bit rate of the ADC  
**Parameters:** rate -  12, 14, 16, 18  
**Returns:** null  
12 = 12 bit (240SPS max)  
14 = 14 bit (60SPS max)  
16 = 16 bit (15SPS max)  
18 = 18 bit (3.75SPS max)  

```
set_conversion_mode(mode)
```
Set the conversion mode for the ADC  
**Parameters:** mode -  0 = One-shot conversion, 1 = Continuous conversion  
**Returns:** null

Usage
====

To use the ADC Differential Pi library in your code you must first import the library:
```
from ADCDifferentialPi import ADCDifferentialPi
```
Next, you must initialise the ADCDifferentialPi object:
```
adc = ADCDifferentialPi(0x68, 0x69, 18)
```
The first two arguments are the I2C addresses of the ADC chips. The values shown are the default addresses of the ADC board.  

The third argument is the sample bit rate you want to use on the ADC chips. The sample rate can be 12, 14, 16 or 18  


You can now read the voltage from channel 1 with:  
```
adc.read_voltage(1)
```
