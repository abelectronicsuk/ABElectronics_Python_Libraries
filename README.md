AB Electronics Python Libraries
=====

Python Libraries to work with Raspberry Pi expansion boards from https://www.abelectronics.co.uk

**Important:**
This library supports Python 3 only.
If you require a version compatible with Python 2, it is available in our archive repository at https://github.com/abelectronicsuk/ABElectronics_Python2_Libraries.

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

To use a specific part of our Python library in your project without installing the entire library, you can copy the necessary class file into your project's directory. For example, to use the IO Pi Plus, copy the **IOPi.py** file from the **IOPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly use the class's functionality in your project.

```bash
from IOPi import IOPi
```

To configure the SPI bus, follow our [SPI and Python on Raspberry Pi OS](https://www.abelectronics.co.uk/kb/article/2/spi-and-raspbian-linux-on-a-raspberry-pi) tutorial.

To configure the I2C bus, follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

### ADCDACPi
This directory contains ADC DAC Pi Python Library with ADC read and DAC write demos to use with the [ADC DAC Pi](https://www.abelectronics.co.uk/p/74/adc-dac-pi-zero)  
### ADCPi 
This directory contains ADC Pi Python Library and demos to use with the [ADC Pi](https://www.abelectronics.co.uk/p/69/adc-pi)  
### ADCDifferentialPi 
This directory contains ADC Differential Pi Python Library and demos to use with the [ADC Differential Pi](https://www.abelectronics.co.uk/p/65/adc-differential-pi)  
This library is also compatible with the [Delta-Sigma Pi](https://www.abelectronics.co.uk/kb/article/1041/delta-sigma-pi)  
### ExpanderPi
This directory contains IO Pi Python Library and demos to use with the [Expander Pi](https://www.abelectronics.co.uk/p/50/expander-pi)  
### I2C Switch  
This directory contains the I2C Switch Python library and demo to use with the 4-channel [I2C switch](https://www.abelectronics.co.uk/p/84/i2c-switch "I2C Switch")  
### IOPi
This directory contains IO Pi Python Library and demos to use with the [IO Pi Plus](https://www.abelectronics.co.uk/p/54/io-pi-plus)  
### IOZero32
This directory contains IO Zero 32 Python Library and demos to use with the [IO Zero 32](https://www.abelectronics.co.uk/p/86/io-zero-32)  
### RTCPi
This directory contains RTC Pi Python Library and demos to use with the [RTC Pi](https://www.abelectronics.co.uk/p/70/rtc-pi)  
### ServoPi
This directory contains ServoPi Python Library and demos to use with the [Servo Pi](https://www.abelectronics.co.uk/p/72/servo-pwm-pi)  

A previous version of the Python libraries compatible with Python 2.7 can be found at https://github.com/abelectronicsuk/ABElectronics_Python2_Libraries
