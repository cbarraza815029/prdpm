# Description
Pi Remote Device Power Management Tool (prdpm) is a python script intended to run on Raspberry Pi SBCs equipped with a 40-pin GPIO header.

This project was designed to control a single device with an ATX Controller board attached to a Pi. Any Pi with a 40-pin GPIO header and an ATX Controller board should work (might need to modify code). Modification will not be neccessary if using a controller board from https://perdeas.com/wp/?p=36.

Will need to install gpiozero Python library if not already installed.

# How to use
Once running, prdpm will prompt you for a command. You can choose from the following:
o(n)     : Turn on device
o(ff)    : Turn off device
r(eset)  : Reset device
s(tatus) : Display device status (on/off)
h(elp)   : Display list of commands
e(xit)   : Exit Remote Device Power Management

Any input other than the above will give you the message "Command not supported. Type 'h(elp)' for list of commands."

# Individual Module Descriptions (coming soon)