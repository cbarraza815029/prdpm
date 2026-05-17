# Description
Pi Remote Device Power Management Tool (prdpm) is a python script intended to run on Raspberry Pi SBCs equipped with a 40-pin GPIO header.

This project was designed to control a single device with a Pi via an ATX Controller board. Any board should work although you will need to make modifications to the code if you're not using the controller board from https://perdeas.com/wp/?p=36.

# Requirements
* Python 3.9 or newer
* gpiozero
* lgpio
* rpi.gpio

NOTE: The above come pre-installed in Raspberry Pi OS.

# How to use
On linux, cd to where you cloned prdpm and then run **python3 ./prdpm.py** OR run **python3 /path/to/prdpm/prdpm.py**.

Once running, prdpm will prompt you for a command. You can choose from the following:
```
o(n)     : Turn on device
o(ff)    : Turn off device
r(eset)  : Reset device
s(tatus) : Display device status (on/off)
c(hange) : Change IP address or hostname of device
h(elp)   : Display list of commands
e(xit)   : Exit Remote Device Power Management
```
The parentheses mean that part of the command is optional (e.g. you can type "s" <ins>or</ins> "status" to see if a device is on or off). Any input other than the above will give you the message "Command not supported. Type 'h(elp)' for list of commands."

# Individual Module Descriptions
## prdpm.py
The prdpm script that contains all functions necessary to remotely power on or off a PC. Also contains descriptions for each function.

## vars.py
The module that contains commonly used variables. Changes made here will apply to the entire program (e.g. changing target_host from "freenas.local" to "file-server.net" will change the device being pinged; Pi must be hooked up to the new device for prdpm to continue working). The variables are:

### pwr variable
The variable assigned to the GPIO pin connected to the ATX front panel power switch via the controller board. The gpiozero library uses Broadcom (BCM) pin numbering for the GPIO pins (see https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering); set to BCM pin 23 (i.e. board pin 16) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### pwr_rst variable
The variable assigned to the GPIO pin connected to the ATX front panel reset switch via the controller board. Set to BCM pin 27 (i.e. board pin 13) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### target_host variable
The variable assigned to the IP address or hostname of target device. Used to tell whether the device is already on or off. Set to "freenas.local" by default; change this to the IP address or hostname of the device you want to power on or off.