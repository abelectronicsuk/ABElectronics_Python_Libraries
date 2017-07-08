#!/usr/bin/env python
"""
================================================
ABElectronics Servo Pi pwm controller | PWM servo controller demo

run with: python demo_servomove.py
================================================

This demo shows how to set the limits of movement on a servo
and then move between those positions
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time

try:
    from ServoPi import PWM
except ImportError:
    print("Failed to import ServoPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from ServoPi import PWM
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main():
    """
    Main program function
    """
    pwm = PWM(0x40)

    # set the servo minimum, centre and maximum limits
    servo_min = 250  # Min pulse length out of 4096
    servo_med = 400  # Min pulse length out of 4096
    servo_max = 500  # Max pulse length out of 4096

    # Set PWM frequency to 60 Hz
    pwm.set_pwm_freq(60)
    pwm.output_enable()

    while True:
        # Move servo on port 0 between three points
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(0.5)
        pwm.set_pwm(0, 0, servo_med)
        time.sleep(0.5)
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(0.5)
        # use set_all_pwm to set PWM on all outputs

if __name__ == "__main__":
    main()
