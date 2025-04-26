AB Electronics UK ADC Differential Pi Python Library
=====

This Python Library is for use with ADC Differential Pi Raspberry Pi expansion board from  
https://www.abelectronics.co.uk  

The ADC Differential Pi is an 18-bit, 8-channel, I2C ADC board that can be used to read analogue voltages from sensors and other devices. It uses the Microchip MCP3424 Delta-Sigma ADC chip and can be used with any Raspberry Pi model that has a 40-pin GPIO connector, along with other compatible small board computers.  

The library provides functions to read the voltage from the ADC channels, set the gain of the PGA, set the bit mode of the ADC and set the conversion mode of the ADC.

For more information on the ADC Differential Pi board, please visit the product page at https://www.abelectronics.co.uk/p/65/adc-differential-pi

For user guides and troubleshooting tips, please visit our knowledge base at https://www.abelectronics.co.uk/kb/article/1130/adc-differential-pi

The example python files can be found in /ABElectronics_Python_Libraries/ADCDifferentialPi/demos  

### Table of Contents
1. [Downloading and Installing the Library](#downloading-and-installing-the-library)
   - [Using Classes Without Installing the Library](#using-classes-without-installing-the-library)
2. [Software Requirements](#software-requirements)
3. [Classes](#classes)
   - [ADCDifferentialPi](#ADCDifferentialPiclass)
4. [Functions](#functions)
   - [read_voltage](#read_voltage)
   - [read_raw](#read_raw)
   - [set_pga](#set_pga)
   - [set_bit_mode](#set_bit_mode)
   - [set_conversion_mode](#set_conversion_mode)
   - [set_i2c_address1](#set_i2c_address1)
   - [set_i2c_address2](#set_i2c_address2)
   - [get_i2c_address1](#get_i2c_address1)
   - [get_i2c_address2](#get_i2c_address2)
5. [Quick Start](#quickstart)

---

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

<a id="using-classes-without-installing-the-library"></a>
#### Using classes without installing the library.

The ADC Differential Pi library is located in the ADCDifferentialPi directory  

To use a specific part of our Python library in your project without installing the entire library, you can copy the necessary class file into your project's directory. For example, to use the ADC Differential Pi, copy the **ADCDifferentialPi.py** file from the **ADCDifferentialPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly utilize the class's functionality in your project.

```python
from ADCDifferentialPi import ADCDifferentialPi
```
 
<a id="software-requirements"></a>
#### Software Requirements

The library requires I2C to be enabled on the Raspberry Pi and the smbus2 or python3-smbus Python library to be installed.  

```bash
sudo pip3 install smbus2
```

To configure the I2C bus, follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

<a id="classes"></a>
# Classes:

<a id="ADCDifferentialPiclass"></a>
## ADCDifferentialPi Class
```python
ADCDifferentialPi(address, address2, mode, bus)
```
**Parameters:**  
address: I2C address for channels 1 to 4, 0x68 to 0x6F. Defaults to 0x68  
address2: I2C address for channels 5 to 8, 0x68 to 0x6F. Defaults to 0x69  
mode: bit-mode, values can be 12, 14, 16 or 18. Defaults to 18-bit resolution.  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.  

<a id="functions"></a>
## Functions:

<a id="read_voltage"></a>
### read_voltage
```python
read_voltage(channel) 
```

**Parameters:** channel - 1 to 8  
**Returns:** number as a float between 0 and 5.0  

Read the voltage from the selected channel.   

<a id="read_raw"></a>
### read_raw
```python
read_raw(channel) 
```

**Parameters:** channel - 1 to 8  
**Returns:** number as an int

Read the raw int value from the selected channel  

<a id="set_pga"></a>
### set_pga
```python
set_pga(gain)
```
 
**Parameters:** gain - 1, 2, 4, 8  
**Returns:** null  

Set the gain of the PGA on the chip 

<a id="set_bit_mode"></a>
### set_bit_mode
```python
set_bit_mode(mode)
```
**Parameters:** mode - 12, 14, 16, 18  
**Returns:** null  
12 = 12 bit (240SPS max)  
14 = 14 bit (60SPS max)  
16 = 16 bit (15SPS max)  
18 = 18 bit (3.75SPS max)  

Set the sample bit mode of the ADC. The ADC Differential Pi can be set to 12, 14, 16 or 18 bits. The default is 18 bits. Higher bit modes provide more accurate readings, but they also require more processing time and can take longer to get a reading. Lower bit modes provide less accurate readings, but they are faster.


<a id="set_conversion_mode"></a>
### set_conversion_mode
```python
set_conversion_mode(mode)
```

**Parameters:** mode -  0 = One-shot conversion, 1 = Continuous conversion  
**Returns:** null  

Set the conversion mode for the ADC. The ADC Differential Pi can be set to one-shot or continuous conversion mode.  

One shot mode is useful for applications where you only need to take a single reading at a time, such as when measuring the voltage of a battery. Continuous mode is useful for applications where you need to take multiple readings in quick succession, such as when measuring the temperature of a sensor. One shot mode has lower power consumption than in continuous mode, but it may take longer to get a reading. Continuous mode has a higher power consumption, but it can provide faster readings.


<a id="set_i2c_address1"></a>
### set_i2c_address1
```python
set_i2c_address1(address)
```

**Parameters:** address - 0x68 to 0x6F  
**Returns:** null  

Set the I2C address for the ADC on channels 1 to 4  

<a id="set_i2c_address2"></a>
### set_i2c_address2
```python
set_i2c_address2(address)
```

**Parameters:** address - 0x68 to 0x6F  
**Returns:** null  

Set the I2C address for the ADC on channels 5 to 8  

<a id="get_i2c_address1"></a>
### get_i2c_address1
```python
get_i2c_address1()
```
 
**Returns:** I2C address  

Gets the I2C address for the ADC on channels 1 to 4  

<a id="get_i2c_address2"></a>
### get_i2c_address2
```python
get_i2c_address2()
```
**Returns:** I2C address  

Gets the I2C address for the ADC on channels 5 to 8  

<a id="quickstart"></a>
## Quick Start

If you're familiar with Python and Raspberry Pi, here's how to get up and running quickly:


### 1. Import the library  

   To use the ADC Differential Pi library in your code, you must first import the ADCDifferentialPi class from the ADCDifferentialPi library:
```python
from ADCDifferentialPi import ADCDifferentialPi
```

### 2. Initialise the ADCDifferentialPi Object  
   Create an instance of the ADCDifferentialPi class by specifying the I2C addresses and bit mode:
```python
adc = ADCDifferentialPi(0x68, 0x69, 18)
```
The first two arguments are the I2C addresses of the ADC chips. The values shown are the default addresses of the ADC Differential Pi board.  

The third argument is the bit mode you want to use on the ADC chips. The sample mode can be 12, 14, 16 or 18 bits. The default is 18 bits.

### 3. Read Voltage from a Channel  
Use the read_voltage method to read the voltage from a specific channel:
```python
adc.read_voltage(1)
```
Replace 1 with the desired channel number (1 to 8).