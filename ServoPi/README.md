AB Electronics UK Servo Pi Python Library
=====

Python Library to use with Servo Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

The example python files can be found in /ABElectronics_Python_Libraries/ServoPi/demos  

### Downloading and Installing the library

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```

To install the python library navigate into the ABElectronics_Python_Libraries folder and run:  

For Python 2.7:
```
sudo python setup.py install
```
For Python 3.4:
```
sudo python3 setup.py install
```

If you have PIP installed you can install the library directly from github with the following command:

For Python 2.7:
```
python2.7 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python3_Libraries.git
```

For Python 34:
```
python3.4 -m pip install git+https://github.com/abelectronicsuk/ABElectronics_Python3_Libraries.git
```

The Servo Pi library is located in the ServoPi directory

The library requires python-smbus to be installed.  
For Python 2.7:
```
sudo apt-get install python-smbus
```
For Python 3.4:
```
sudo apt-get install python3-smbus
```

Functions:
----------

```
set_pwm_freq(freq) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency  
**Returns:** null  

```
set_pwm(channel, on, off) 
```
Set the output on single channels  
**Parameters:** channel - 1 to 16, on - time period, off - time period  
**Returns:** null  


```
set_all_pwm( on, off) 
```
Set the output on all channels  
**Parameters:** on - time period, off - time period  
**Returns:** null  

```
output_disable()
```
Disable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
output_enable()
```
Enable the output via OE pin  
**Parameters:** null  
**Returns:** null  

```
set_allcall_address(address)
```
Set the I2C address for the All Call function  
**Parameters:** address  
**Returns:** null  

```
enable_allcall_address()
```
Enable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```
disable_allcall_address()
```
Disable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  



Usage
====

To use the Servo Pi library in your code you must first import the library:
```
from ServoPi import PWM
```
Next you must initialise the ServoPi object:
```
pwm = PWM(0x40)
```
Set PWM frequency to 60 Hz
```
pwm.set_pwm_freq(60)  
pwm.output_enable()
```
Set three variables for pulse length
```
servoMin = 250  # Min pulse length out of 4096
servoMed = 400  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096
```
Loop to move the servo on port 0 between three points
```
while True:
  pwm.set_pwm(0, 0, servoMin)
  time.sleep(0.5)
  pwm.set_pwm(0, 0, servoMed)
  time.sleep(0.5)
  pwm.set_pwm(0, 0, servoMax)
  time.sleep(0.5)
  # use set_all_pwm to set PWM on all outputs
```
