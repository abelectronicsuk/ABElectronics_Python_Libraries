#!/usr/bin/python

from ABElectroncs_ServoPi import PWM
import time

# Initialise the PWM device using the default address, change this value if you have bridged the address selection jumpers
pwm = PWM(0x40)



servoMin = 250  # Min pulse length out of 4096
servoMed = 400  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096

# Set PWM frequency to 60 Hz
pwm.setPWMFreq(60)                        


while (True):
  # Move servo on port 0 between three points
  pwm.setPWM(0, 0, servoMin)
  time.sleep(0.5)
  pwm.setPWM(0, 0, servoMed)
  time.sleep(0.5)
  pwm.setPWM(0, 0, servoMax)
  time.sleep(0.5)
  # use setAllPWM to set PWM on all outputs