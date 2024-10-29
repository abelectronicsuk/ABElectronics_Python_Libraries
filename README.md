AB Electronics Python Libraries
=====

Python Libraries to work with Raspberry Pi expansion boards from https://www.abelectronics.co.uk


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

To use a specific part of our Python library in your project without installing the entire library, you can simply copy the needed class file into your project's directory. For example, to use the IO Pi Plus, copy the **IOPi.py** file from the **IOPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly utilize the class's functionality in your project.

```
from IOPi import IOPi
```

To configure the SPI bus follow our [SPI and Python on Raspberry Pi OS](https://www.abelectronics.co.uk/kb/article/2/spi-and-raspbian-linux-on-a-raspberry-pi) tutorial.

To configure the I2C bus follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

### ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the [ADC DAC Pi](https://www.abelectronics.co.uk/p/74/adc-dac-pi-zero)  
### ADCPi 
This directory contains ADC Pi Python Library  and demos to use with the [ADC Pi](https://www.abelectronics.co.uk/p/69/adc-pi)  
### ADCDifferentialPi 
This directory contains ADC Differential Pi Python Library and demos to use with the [ADC Differential Pi](https://www.abelectronics.co.uk/p/65/adc-differential-pi)  
This library is also compatible with the [Delta-Sigma Pi](https://www.abelectronics.co.uk/kb/article/1041/delta-sigma-pi)  
### ExpanderPi
This directory contains IO Pi Python Library  and demos to use with the [Expander Pi](https://www.abelectronics.co.uk/p/50/expander-pi)  
### I2C Switch  
This directory contains the I2C Switch Python library and demo to use with the 4-channel [I2C switch](https://www.abelectronics.co.uk/p/84/i2c-switch "I2C Switch")  
### IOPi
This directory contains IO Pi Python Library and demos to use with the [IO Pi Plus](https://www.abelectronics.co.uk/p/54/io-pi-plus)  
### IOZero32
This directory contains IO Zero 32 Python Library and demos to use with the [IO Zero 32](https://www.abelectronics.co.uk/p/86/io-zero-32)  
### RTCPi
This directory contains RTC Pi Python Library and demos to use with the [RTC Pi](https://www.abelectronics.co.uk/p/70/rtc-pi)  
### ServoPi
This directory contains ServoPi Python Library  and demos to use with the [Servo Pi](https://www.abelectronics.co.uk/p/72/servo-pwm-pi)  

#### 07-07-2017 Changes for Version 2.0

Version 2.0.0 of the Python library has introduced several changes to the structure of the classes and demo files.  The major changes are listed below.  Please read CHANGELOG.md for a complete list of changes.

* Files renamed: removed ABE_ from all names.  
ABE_ADCDACPi > ADCDACPi  
ABE_ADCDifferentialPi > ADCDifferentialPi  
ABE_ADCPi > ADCPi  
ABE_ExpanderPi > ExpanderPi  
ABE_IOPi > IOPi  
ABE_RTCPi > RTCPi  
ABE_ServoPi >  ServoPi

* All classes and demo files are now compatible with Python 2 and 3.  The ABElectronics_Python3_Libraries will no longer be updated so please use this version instead for your Python 3 projects.
* Moved all demo files into demo sub-folders for each class
* The ABE_Helper class has been integrated into the board classes and does not need to be imported separately.
* Added a setup.py into the root for installing the library into the main Python library directory.

Previous versions of the Python libraries can be found at https://github.com/abelectronicsuk/Archive
