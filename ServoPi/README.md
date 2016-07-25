AB Electronics UK Servo Pi Python Library
=====

Python Library to use with Servo Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

Install
====

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git
```
The Servo Pi library is located in the ServoPi directory

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/ServoPi/
```

The library requires i2c to be enabled and python-smbus to be installed.

Follow the tutorial at [https://www.abelectronics.co.uk/kb/article/1/i2c--smbus-and-raspbian-linux](https://www.abelectronics.co.uk/kb/article/1/i2c--smbus-and-raspbian-linux) to enable i2c and install python-smbus.

The example python files in /ABElectronics_Python_Libraries/ServoPi/ will now run from the terminal.

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
from ABE_ServoPi import PWM
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
while (True):
  pwm.set_pwm(0, 0, servoMin)
  time.sleep(0.5)
  pwm.set_pwm(0, 0, servoMed)
  time.sleep(0.5)
  pwm.set_pwm(0, 0, servoMax)
  time.sleep(0.5)
  # use set_all_pwm to set PWM on all outputs
```
