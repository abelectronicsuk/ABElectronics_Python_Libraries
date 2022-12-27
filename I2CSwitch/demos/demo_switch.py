#!/usr/bin/env python
"""
================================================
AB Electronics UK I2CSwitch | Channel select demo

run with: python demo_switch.py -c 1
================================================

This demo shows how to set the I2C output channel 
using a command line parameter.

Specify the parameter -c or --channel as a number 1 to 4
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals

import sys, getopt

try:
    from I2CSwitch import I2CSwitch
except ImportError:
    print("Failed to import I2CSwitch from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from I2CSwitch import I2CSwitch
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")


def main(argv):
    """
    Main program function
    """

    # create an instance of the I2CSwitch class on i2c address 0x70
    i2cswitch = I2CSwitch(0x70)

    #reset the switch
    i2cswitch.reset()

    channelparam = 0

    try:
        opts, args = getopt.getopt(argv, "hc:", ["channel="])
    except getopt.GetoptError:
        print('demo_switch.py -c <channel>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -c <channel>')
            sys.exit()
        elif opt in ("-c", "--channel"):
            try:
                channelparam = int(arg)                
            except ValueError:
                print('error: channel must be between 1 and 4')
                sys.exit(2)

    if (channelparam < 1 or channelparam > 4):
        print('error: channel must be between 1 and 4')
        sys.exit(2)
    else:
        # Set the I2C channel
        i2cswitch.switch_channel(channelparam)

        # Get the state of the selected channel from the I2C switch
        status = i2cswitch.get_channel_state(channelparam)

        # Print the result from get_channel_state()
        if status is True:
            print('Channel set to ', channelparam)
        else:
            print('Error setting channel')


if __name__ == "__main__":
    main(sys.argv[1:])
