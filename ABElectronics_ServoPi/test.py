#!/usr/bin/python

from ABElectronics_ServoPi import PWM
import time

# Initialise the PWM device using the default address, change this value if you have bridged the address selection jumpers
pwm = PWM(0x40)



servoMin = 250  # Min pulse length out of 4096
servoMed = 400  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096

# Set PWM frequency to 60 Hz
pwm.setPWMFreq(60)                        


while (True):

  for x in range(150, 600, 1):
    pwm.setPWM(0, 0, x)
    time.sleep(0.01)
  for x in range(600, 150, -1):
    pwm.setPWM(0, 0, x)
    time.sleep(0.01)  
