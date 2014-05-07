IO Pi
=====

Python library for using the IO Pi Raspberry Pi expansion boards from http://www.abelectronics.co.uk

This library gives you control over most of the features available on the Microchip MCP23017 IO controller.  Features include setting pin direction, writing to and read from a pin or port,  enabling pull-up resistors and using the interrupt pins.

Example code is available in the demo folder and each method in the python library is commented with a description of its function and available parameters.


Getting Started
=====

To download the IO Pi python library to your Raspberry Pi type in terminal:

```
git clone https://github.com/abelectronicsuk/ABElectroncs_Python_Libraries.git
```

The library requires python-smbus to be installed.
```
sudo apt-get update
sudo apt-get install python-smbus
```

Add the location where you downloaded the python libraries into PYTHONPATH

```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectroncs_Python_Libraries/ABElectroncs_IOPi/
```

The example python files in /ABElectroncs_Python_Libraries/ABElectroncs_IOPi/demos/ should now run.