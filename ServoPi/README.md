AB Electronics UK Servo Pi Python Library
=====

Python Library to use with Servo PWM Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk/p/72/servo-pwm-pi

The Servo PWM Pi is based on the NXP PCA9685 PWM controller.

For user guides and troubleshooting tips, please visit our knowledge base at https://www.abelectronics.co.uk/kb/article/1136/servo-pwm-pi

The example python files can be found in /ABElectronics_Python_Libraries/ServoPi/demos  

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

The Servo Pi library is located in the ServoPi directory

To use a specific part of our Python library in your project without installing the entire library, you can copy the necessary class file into your project's directory. For example, to use the Servo Pi, copy the **ServoPi.py** file from the **ServoPi** directory to where your project files are located. After doing this, you can use the class in your program by adding an import statement at the beginning of your Python code. This allows you to directly use the class's functionality in your project.

```python
from ServoPi import ServoPi
```

#### Software Requirements

The library requires I2C to be enabled on the Raspberry Pi and the smbus2 or python3-smbus Python library to be installed.  

```bash
sudo pip3 install smbus2
```

To configure the I2C bus, follow our [Enabling I2C on the Raspberry Pi](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi) tutorial.

# Class: PWM #
```python
PWM(address, bus)
```
The PWM class provides control over the pulse-width modulation outputs on the PCA9685 controller.  Functions include setting the frequency and duty cycle for each channel.  

**Parameters:**  
address (optional): device I2C address, defaults to 0x40  
bus (optional): I2C bus number (integer).  If no value is set the class will try to find the I2C bus automatically using the device name.  

Initialise with the I2C address for the Servo Pi.

```python
pwmobject = PWM(0x40)
```

Functions:
----------

```python
set_pwm_freq(freq, calibration) 
```
Set the PWM frequency  
**Parameters:** freq - required frequency, calibration - optional integer value to offset oscillator errors.  
**Returns:** null  

```python
set_pwm(channel, on, off) 
```
Set the output on single channels  
**Parameters:** channel - 1 to 16, on-time period 0 to 4095, off-time period 0 to 4095.  Total on-time and off-time cannot exceed 4095  
**Returns:** null  

```python
set_pwm_on_time(channel, on_time) 
```
Set the output on time for a single channels  
**Parameters:** channel - 1 to 16, on - period 0 to 4095  
**Returns:** null  

```python
set_pwm_off_time(self, channel, off_time) 
```
Set the output off time for a single channels  
**Parameters:** channel - 1 to 16, off_time - period 0 to 4095  
**Returns:** null  

```python
get_pwm_on_time(channel) 
```
Get the output on time for a single channels  
**Parameters:** channel - 1 to 16  
**Returns:** on time - integer 0 to 4095  

```python
get_pwm_off_time(channel) 
```
Get the output off time for a single channels  
**Parameters:** channel - 1 to 16  
**Returns:** on time - integer 0 to 4095  


```python
set_all_pwm(on, off) 
```
Set the output on all channels  
**Parameters:** on-time period, off-time period 0 to 4095.  Total on-time and off-time cannot exceed 4095  
**Returns:** null  

```python
output_disable()
```
Disable the output via the OE pin  
**Parameters:** null  
**Returns:** null  

```python
output_enable()
```
Enable the output via the OE pin  
**Parameters:** null  
**Returns:** null  

```python
set_allcall_address(address)
```
Set the I2C address for the All Call function  
**Parameters:** address  
**Returns:** null  

```python
enable_allcall_address()
```
Enable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```python
disable_allcall_address()
```
Disable the I2C address for the All Call function  
**Parameters:** null  
**Returns:** null  

```python
sleep()
```
Puts the PCA9685 PWM controller into a sleep state.  
**Parameters:** null  
**Returns:** null  

```python
wake()
```
Wakes the PCA9685 PWM controller from its sleep state.  
**Parameters:** null  
**Returns:** null  

```python
is_sleeping()
```
Returns if the PCA9685 PWM controller is in its sleep state.  
**Parameters:** null  
**Returns:** True = Is sleeping, False = Is awake.  

```python
invert_output(state)
```
Inverts the outputs on all PWM channels.  
**Parameters:** True = inverted, False = non-inverted  
**Returns:** null  

# Class: Servo #
```python
Servo(address, low_limit, high_limit, reset, bus)
```
The Servo class provides functions for controlling the position of servo motors commonly used on radio control models and small robots.  The Servo class initialises with a default frequency of 50 Hz and low and high limits of 1.0 ms and 2.0 ms. 

Initialise with the I2C address for the Servo Pi.

```python
servo_object = Servo(0x40)
```
**Optional Parameters:**  
low_limit = Pulse length in milliseconds for the lower servo limit. (default = 1.0 ms)  
high_limit = Pulse length in milliseconds for the upper servo limit. (default = 2.0 ms)  
reset = True: reset the servo controller and turn off all channels.  False: initialise with existing servo positions and frequency. (default = true)  
bus: I2C bus number (integer).  If no value is set the class will try to find the i2c bus automatically using the device name.   

Functions:
----------

```python
move(channel, position, steps=250) 
```
Set the servo position  
**Parameters:**  
channel - 1 to 16  
position - value between 0 and the maximum number of steps.  
steps (optional) - The number of steps between the low and high servo limits.  This value is pre-set at 250 but can be any number between 0 and 4095.  On a typical RC servo, a step value of 250 is recommended.  
**Returns:** null  

```python
get_position(channel, steps=250) 
```
Get the servo position  
**Parameters:** 
channel - 1 to 16  
steps (optional) - The number of steps between the low and high servo limits.  This value is pre-set at 250 but can be any number between 0 and 4095.  On a typical RC servo, a step value of 250 is recommended.  
**Returns:** position - value between 0 and the maximum number of steps. Due to rounding errors when calculating the position, the returned value may not be the same as the set value. 

```python
set_low_limit(low_limit, channel)
```
Set the pulse length for the lower servo limits.  Typically, 1.0 ms.  
Warning: Setting the pulse limit below 1.0 ms may damage your servo.  
**Parameters:**  
low_limit - Pulse length in milliseconds for the lower servo limit.  
channel (optional) - The channel for which the low limit will be set.  
If this value is omitted, the low limit will be set for all channels.  
**Returns:** null  

```python
set_high_limit(high_limit, channel)
```
Set the pulse length for the upper servo limits.  Typically, 2.0 ms. 
Warning: Setting the pulse limit above 2.0 ms may damage your servo.  
**Parameters:**  
high_limit - Pulse length in milliseconds for the upper servo limit.  
channel (optional) - The channel for which the upper limit will be set.  
If this value is omitted, the upper limit will be set for all channels.  
**Returns:** null  

```python
set_frequency(freq, calibration) 
```
Set the PWM frequency  
**Parameters:**  
freq - required frequency for the servo.  
calibration - optional integer value to offset oscillator errors.  
**Returns:** null  

```python
output_disable()
```
Disable the output via the OE pin  
**Parameters:** null  
**Returns:** null  

```python
output_enable()
```
Enable the output via the OE pin  
**Parameters:** null  
**Returns:** null  

```python
sleep()
```
Puts the PCA9685 PWM controller into a sleep state.  
**Parameters:** null  
**Returns:** null  

```python
wake()
```
Wakes the PCA9685 PWM controller from its sleep state.  
**Parameters:** null  
**Returns:** null  

```python
is_sleeping()
```
Returns if the PCA9685 PWM controller is in its sleep state.  
**Parameters:** null  
**Returns:** True = Is sleeping, False = Is awake.  

Usage
====

**PWM Class**

To use the Servo Pi PWM class in your code, you must first import the class:
```python
from ServoPi import PWM
```
Next, you must initialise the PWM object:
```python
pwm = PWM(0x40)
```
Set the PWM frequency to 200 Hz and enable the output
```python
pwm.set_pwm_freq(200)  
pwm.output_enable()  
```
Set the pulse width of channel 1 to 1024 or 25% duty cycle
```python
pwm.set_pwm(1, 0, 1024) 
```

**Servo Class**

To use the Servo Pi Servo class in your code, you must first import the class:
```python
from ServoPi import Servo
```
Next, you must initialise the Servo object:
```python
servo = Servo(0x40)
```
Set PWM frequency to 50 Hz
```python
servo.set_frequency(50)  
```
Move the servo on channel 1 to position 125 out of 250 steps  
```python
servo.move(1, 125, 250)
```

