## 2025-04-22 Andrew Dorey  

* 2.5.3 Changes to ADC Differential Pi and ADC Pi libraries.
 
  * Added note in the header of the ADC Pi library about effective resolution being 11, 13, 15 and 17 bits in single-ended mode
  * Renamed set_bit_rate method to set_bit_mode in the ADC Pi library. Made a set_bit_rate wrapper to keep compatability with existing code.
  * Improved docstrings for all methods with comprehensive descriptions
  * Added type hints to method signatures for better IDE support
  * Updated copyright year to 2025 and added licence information
  * Fixed a bug in set_conversion_mode where ADC2 configuration wasn't properly updated
  * Improved error handling for I2C bus communication failures
  * Enhanced timeout mechanism to be more reliable on various hardware platforms
  * Added ADCTimeoutError class for conversion timeout scenarios
  * Enhanced I2C bus detection for a wider range of single-board computers
  * Implemented more robust device detection logic


## 2025-03-28 Andrew Dorey  

* 2.5.2 Changes to ADC Differential Pi library based on feedback from raphaelcno https://github.com/abelectronicsuk/ABElectronics_Python_Libraries/issues/31 Renamed set_bit_rate method to set_bit_mode. Made a set_bit_rate wrapper to keep compatability with existing code.

## 2024-10-29 Andrew Dorey  

* 2.5.1 Updated installation instructions in README files.

## 2024-08-13 Andrew Dorey  

* 2.5.0 Cleaned up code. Fixed PEP8 formatting issues. Fixed spelling mistakes. Changed Expander Pi ADC clock speed to 1MHz to increase sample rate.

## 2023-12-27 Andrew Dorey  

* 2.4.9 Added pyproject.toml file to allow the use of python3 build. Updated documentation.

## 2023-10-10 Andrew Dorey  

* 2.4.8 Added Orange Pi Zero 2 support for I2C based expansion boards.

## 2023-02-04 Andrew Dorey  

* 2.4.7 Updates to IO Pi and Expander Pi documentation.

#### 2022-12-27 Andrew Dorey

* 2.4.6 Updated spelling and grammar in the ReadMe files and code comments.

#### 2022-04-23 Andrew Dorey

* 2.4.5 Added a new library for the IO Zero 32 expansion board.

#### 2021-11-19 Andrew Dorey

* 2.4.4 Added new IO Pi Zero demo file demo_ioreadzero.py

#### 2021-10-26 Andrew Dorey

* 2.4.3 Added more exception handling to the ADC Pi class.

#### 2020-12-22 Andrew Dorey

* 2.4.2 Added bus parameter to the ADC Differential Pi, ADC Pi, Expander Pi, I2C Switch, RTC Pi and Servo Pi classes to allow for setting the I2C bus manually.

#### 2020-12-21 Andrew Dorey

* 2.4.2 Added bus parameter to the IO Pi class to allow for setting the I2C bus manually.

#### 2020-09-02 Andrew Dorey

* 2.4.1 Added support for Banana Pi BPI M2 Zero on Raspbian

#### 2020-08-31 Andrew Dorey

* 2.4.0 Fixed bug in Expander Pi library.

#### 2020-08-24 Andrew Dorey

* 2.3.9 Added support for Banana Pi BPI M2 Zero on Ubuntu

#### 2020-07-12 Andrew Dorey

* 2.3.8 Expander Pi bug fix. Added missing __updatebyte() function.

#### 2020-07-12 Andrew Dorey

* 2.3.7 Updates to ADC Pi and ADC Differential Pi libraries.  Updated read_voltage and read_raw to check if the channel is out of bounds.

#### 2020-07-05 omstaal

* 2.3.6 Bug fix in ADC Pi library.  Setting channel 0 or negative in read_raw in ADCPi did not raise a ValueError.  

#### 2020-06-20 Andrew Dorey

* 2.3.5 Updates to IO Pi and Expander Pi libraries.  Added get_ functions for each device register.  Refactored code to reduce repetition in pin, port and bus methods.  Added unit tests for the IO Pi library.  

#### 2020-06-17 Andrew Dorey

* 2.3.4 Added get_port_direction(), get_port_pullups() and get_port_polarity() into the IO Pi and Expander Pi libraries.

#### 2020-06-07 Andrew Dorey

* 2.3.3 Fixed read_pin() bug in IO Pi and Expander Pi libraries.

#### 2020-06-05 Andrew Dorey

* 2.3.2 Fixed bugs in IO Pi and Expander Pi libraries.

#### 2020-06-03 Andrew Dorey

* 2.3.2  Updates to the Expander Pi class.   Added new methods for accessing whole IO bus directly, set_bus_direction(), set_bus_pullups(), write_bus(), read_bus(), invert_bus(), set_interrupt_on_bus().  Updated docstrings for all libraries to use Sphinx format.

#### 2020-06-01 Andrew Dorey

* 2.3.1  Updates to the IO Pi class.  Changed method docstrings to use Sphinx format.  Added new methods for accessing whole bus directly, set_bus_direction(), set_bus_pullups(), write_bus(), read_bus(), invert_bus(), set_interrupt_on_bus().  

#### 2020-05-19 Andrew Dorey
* 2.3.0 Updated the Servo Pi class to check if the RPI.GPIO mode has already been set.

#### 2020-05-06 Andrew Dorey
* 2.2.9 Updated the ADC Pi and ADC Differential Pi classes. Added a class definition for TimeoutError to add support for Python 2.7.

#### 2020-02-02 Andrew Dorey
* 2.2.8 Updated the ADC Expander Pi ADC class. Reduced the SPI speed to improve accuracy.

#### 2020-01-23 Andrew Dorey
* 2.2.7 Updated the ADC Differential Pi and ADC Pi libraries to improve the performance in threaded applications.  Added new speed test demos.

#### 2019-11-28 Andrew Dorey
* 2.2.6 Added library for the 4-channel I2C switch.

#### 2019-08-05 Andrew Dorey
* 2.2.5 Updated Expander Pi demos for the ADC and IO.  demo_adcread.py now reads all 8 channels.

#### 2019-03-14 Andrew Dorey
* 2.2.4 Updated all I2C-based libraries to use smbus2 by default with a fallback to python-smbus if smbus2 is not available.  This update makes the libraries compatible with Python 3.6 and later.

#### 2019-02-20 Andrew Dorey
* 2.2.3 Add two new IO Pi tutorials, tutorial3.py and tutorial4.py.  Removed tutorial3_rpi_interrupts.py.

#### 2019-02-17 Andrew Dorey
* 2.2.2 Updated the IO Pi interrupts demo and the IO Pi readme to improve the clarity of what each function does.

#### 2018-11-06 Andrew Dorey
* 2.2.1 Fixed a bug in the regex code in all of the I2C-based libraries which detects the model of Raspberry Pi being used.

#### 2018-09-28 Andrew Dorey
* 2.2.0 Updates to Servo Pi library adding a reset option to the servo class and updated readme to include usage examples for the PWM and Servo classes.

#### 2018-08-17 Andrew Dorey
* 2.1.9 Updates to Servo Pi library adding new functions for putting the device to sleep and offsetting the pulse value.

#### 2018-08-17 Andrew Dorey
* 2.1.8 Updates to Servo Pi library adding new functions to get the values from PWM and servo positions and improve the accuracy of the clock using a calibration parameter.

#### 2018-05-22 Alan Kinnaman
* 2.1.7 With this change, an error will be thrown if a channel numbered 0 or lower is specified.

#### 2018-05-21 Alan Kinnaman 
* 2.1.6 If the ADC is defective, it might never set the ready flag.  With this change, an exception is raised if the ADC doesn’t set the ready bit within a reasonable amount of time.

#### 2018-04-26 qpeten 
* 2.1.5 When importing this library in a project which does not use the SPI bus, the library raised an exception on import.
This commit fixes that bug by moving the access to the SPI bus to __init__().

#### 2018-03-15 Andrew Dorey
* 2.1.4 Added support for the Orange Pi PC Plus.

#### 2018-03-07 Andrew Dorey
* 2.1.3 Added a new demo for the ADC Pi to read values from two ADC Pi boards and write them to a log file.

#### 2018-01-21 Andrew Dorey
* 2.1.2 Fixed several bugs with the ADC Pi and ADC Differential Pi libraries where the wrong channel was read if the channels were selected in a certain order..

#### 2018-01-17 Andrew Dorey
* 2.1.1 A new demo showing how to use a button to toggle the state of a variable.

#### 2018-01-03 Andrew Dorey
* 2.1.0 Added new functions for getting the port direction, pull-up status and polarity for the IO bus.

#### 2017-12-24 Andrew Dorey
* 2.0.9 Added MQTT read server and client demos. Bug fix on sensor data.

#### 2017-12-23 Andrew Dorey
* 2.0.8 Added MQTT demos.

#### 2017-10-14 Andrew Dorey
* 2.0.7 Bug fixes for the interrupt tutorial.

#### 2017-09-12 Andrew Dorey
* 2.0.6 Fixed a bug with the ServoPi Servo class where it was not validating the channel number correctly.

#### 2017-08-05 Andrew Dorey
* 2.0.5 Changed ADC Pi library so config variables are not stored in a byte array.

#### 2017-08-05 Andrew Dorey
* 2.0.5 Changed ADC Pi library so config variables are not stored in a byte array.

#### 2017-08-01 Andrew Dorey
* 2.0.4 Fixed several bugs with the Expander Pi library where it was saving the wrong values during any pin read or write operation.

#### 2017-07-31 Andrew Dorey
* 2.0.3 Fixed several bugs with the IO Pi library where it was saving the wrong values during any pin read or write operation.

#### 2017-07-29 Andrew Dorey
* 2.0.2 Updates to the ServoPi library.  
* ServoPi - Added Servo class.
* ServoPi - Changed the channel parameters for the PWM and Servo class to 1 to 16 instead of 0 to 15.  This now matches the channel numbering on the Servo PWM Pi Zero.
* ServoPi - Added parameter checks for function inputs.
* ServoPi - updated demo_servomove.py to use the new Servo class.

#### 2017-07-24 Andrew Dorey
* 2.0.1
Fixed a bug with the __init__.py files where the import would work in Python 2 but fail in Python 3. 

#### 2017-07-07 Andrew Dorey
* 2.0.0 Major Update  
Classes renamed: removed ABE_ from all class names.  
ABE_ADCDACPi > ADCDACPi  
ABE_ADCDifferentialPi > ADCDifferentialPi  
ABE_ADCPi > ADCPi  
ABE_DeltaSigmaPi > DeltaSigmaPi  
ABE_ExpanderPi > ExpanderPi  
ABE_IOPi > IOPi  
ABE_RTCPi > RTCPi  
ABE_ServoPi >  ServoPi
* Updated all classes and demo files to be PEP8 compliant
* All classes and demo files are now compatible with Python 2 and 3.
* Added init files to all folders.
* Added setup.py into the root folder to install the package into the correct folder.
* Moved all demo files into demo sub-folders for each class
* Demo files have been rewritten to automatically try and import the parent class from the system library and then if that fails it will import it from the parent folder.
* Replaced all instances of print within the classes and changed it to raise an exception when an error occurs.
* Optimised the set_dac_raw() function in the ADCDACPi and ExpanderPi classes to give a 48% speed improvement.  
* ADCPi - Integrated the ABE_Helper.py into the ADCPi class.  Various optimisations to reduce the number of function calls during each ADC sample operation.  Added new speed test demo.
* ADC Differential Pi - Same changes as the ADC Pi class.
* Removed the Delta-Sigma class.  For Delta-Sigma Pi users please use the ADC 
Differential Pi class which is functionally identical.
* Expander Pi - Various optimisations to make the class fully PEP8 compliant
* IO Pi - Integrated the ABE_Helper.py into the IOPi class.
* RTC Pi - Integrated the ABE_Helper.py into the RTC class.
* Servo Pi - Integrated the ABE_Helper.py into the PWM class.
* Various small bug fixes and spelling mistakes fixed

#### 2017-07-01 Andrew Dorey  
* 1.6.2 Fixed formatting on README.md 
#### 2017-06-30 Andrew Dorey  
* 1.6.1 Fixed whitespace issue.
#### 2017-06-12 Andrew Dorey
* 1.6.0 Fixed mistake in comments.
#### 2017-06-11 Andrew Dorey 
* 1.5.9 Small fixes to the IO section of the readme.
* Updated Expander Pi Library
#### 2017-06-10 Andrew Dorey
* 1.5.8 Fixed mistake in readme.
#### 2017-04-21 Andrew Dorey
* 1.5.7 Bug Fix
* Updated the adc speed demo.
#### 2017-02-12 Brian Dorey
* 1.5.6 Added support for other platforms.
#### 2017-02-07 Brian Dorey
* 1.5.5 Fixed a bug with the IO address.
#### 2017-02-03 Brian Dorey
* 1.5.4 New GUI demo.
#### 2017-01-26 Brian Dorey
* 1.5.3 Minor fixes.
* New RTC memory demo.
#### 2017-01-03 Brian Dorey
* 1.5.2 updated readme.
* Added new functions for reading and writing to the RTC memory.
#### 2016-11-30 Brian Dorey
* 1.5.1 Updated DAC demos.
#### 2016-10-16 Brian Dorey
* 1.5.0 Bug fix.
#### 2016-08-03 Brian Dorey
* 1.4.9 Added get_signbit function.
#### 2016-07-25 Andrew Dorey
* 1.4.8 Updated URLs.
#### 2016-07-19 Andrew Dorey
* 1.4.7 Minor text changes to comments.
* Added data logger example.
#### 2016-06-26 Andrew Dorey
* 1.4.6 Bug fixes
#### 2016-06-24 Andrew Dorey
* 1.4.5 Updated read_adc_voltage() and read_adc_raw().
#### 2016-06-13 Andrew Dorey
* 1.4.4 Updated the Expander Pi library.
#### 2016-05-18 Andrew Dorey
* 1.4.3 Fixed error with the clock frequency.
#### 2016-04-28 Brian Dorey
* 1.4.2 Fixed error in readme.
#### 2016-01-23 Brian Dorey
* 1.4.1 Merge pull request #8 from moeskerv/master.
#### 2016-01-23 Volker Moesker
* 1.4.0 fixed non-working RTC out configuration.
#### 2016-01-19 Brian Dorey
* 1.3.9 New functions added to the Servo Pi library.
#### 2016-01-12 Brian Dorey
* 1.3.8 New ADC speed test.
* Bug Fixes
#### 2015-11-24 Brian Dorey
* 1.3.7 New Interrupts tutorial.
#### 2015-11-21 Brian Dorey
* 1.3.6 Removed demo-iopiread2.py.
#### 2015-10-30 Brian Dorey
* 1.3.5 Bug fix.
* New thermometer Demo.
#### 2015-10-09 Brian Dorey
* 1.3.4 Bug Fix on invert_pin.
#### 2015-10-04 Brian Dorey
* 1.3.3 New demo for the ADXL335 accelerometer.
#### 2015-10-01 Brian Dorey
* 1.3.2 New ADC Differential Pi library.
#### 2015-09-06 Brian Dorey
* 1.3.1 Updated demos and readme.
* Merge pull request #7 from NealTheGitGuy/feature/add_dac_gain_mode.
#### 2015-09-05 Neal Buchmeyer
* 1.3.0 ADCDACPi: Adjust max voltage out based on gain factor.
* ADCDACPi: Bounds check DAC voltage based on max achievable voltage.
* ADCDACPi: Added the ability to configure DAC gain factor.
#### 2015-07-01 Andrew Dorey
* 1.2.9 Fixed spelling mistake.
#### 2015-06-30 Andrew Dorey
* 1.2.9 Updated variable names.
#### 2015-06-26 Andrew Dorey
* 1.2.8 Small text change.
* New IO threading example.
#### 2015-06-09 Andrew Dorey
* 1.2.7 Fixed bug with the ADC conversion.
#### 2015-05-20 Andrew Dorey
* 1.2.6 Updates to HIH4000 demo.
* Added new demo files.
#### 2015-03-29 Andrew Dorey
* Added conversion mode function.
#### 2015-03-17 Andrew Dorey
* 1.2.5 Fixed spelling mistake.
#### 2015-02-25 Andrew Dorey
* 1.2.4 New read-write demo for the IO Pi.
#### 2015-02-23 Brian Dorey
* 1.2.3 Updated readme.
#### 2015-01-20 Brian Dorey
* 1.2.2 Added error detection.
#### 2015-01-19 Brian Dorey
* 1.2.1 Bug fixes.
* Updated comments.
#### 2014-12-09 Brian Dorey
* 1.2.0 Bug fixes.
#### 2014-11-28 Brian Dorey
* 1.1.9 Updated IO Pi tutorials.
#### 2014-11-27 Brian Dorey
* 1.1.8 Updated IOPi tutorial.
* Updated readme.
* New Python Libraries.
#### 2014-11-08 Andrew Dorey
* 1.1.7 Bug fixes and new test script.
#### 2014-11-07 Andrew Dorey
* 1.1.6 Bug Fix.
#### 2014-11-03 Andrew Dorey
* 1.1.5 Bug Fix.
#### 2014-10-07 Andrew Dorey
* 1.1.4 Bug fix on the readVoltage method.
#### 2014-08-21 Andrew Dorey
* 1.1.3 Added new Expander Pi library.
#### 2014-07-15 Andrew Dorey
* 1.1.2 Added ACS712 Demo.
#### 2014-05-23 Andrew Dorey
* 1.1.1 Optimised ADC Pi library.
#### 2014-05-19 Andrew Dorey
* 1.1.0 Updated README.md.
* New RTC Pi library.
#### 2014-05-18 Andrew Dorey
* 1.0.9 Updated README.md files.
* Update ABElectronics_ServoPi.py.
#### 2014-05-17 Andrew Dorey
* 1.0.8 New ADCDAC library.
* Update README.md.
#### 2014-05-11 Andrew Dorey
* 1.0.7 New tutorial for the IO Pi.
* Bug fix in IO Pi library.
* Added data logger demo.
* IO Pi tutorials added.
#### 2014-05-10 Brian Dorey
* 1.0.6 Update README.md.
#### 2014-05-09 Andrew Dorey
* 1.0.5 Updated ADC-Pi and Delta-Sigma Pi libraries and README.md.
#### 2014-05-07 Brian Dorey
* 1.0.4 Update README.md and fixed spelling mistakes.
#### 2014-05-02 Andrew Dorey
* 1.0.3 Updated IO Pi library.
#### 2014-04-03 Brian Dorey
* 1.0.2 Update to servo pi code.
#### 2014-02-09 Brian Dorey
* 1.0.1 Added IOPi lib and demos.
#### 2014-02-01 Brian Dorey
* 1.0.0 Upload of initial code.
