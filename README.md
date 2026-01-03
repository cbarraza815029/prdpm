# Description
Pi Remote Device Power Management Tool (prdpm) is a python script intended to run on Raspberry Pi SBCs equipped with a 40-pin GPIO header.

This project was designed to control a single device with an ATX Controller board attached to a Pi. Any Pi with a 40-pin GPIO header and an ATX Controller board should work (might need to modify code). Modification will not be neccessary if using a controller board from https://perdeas.com/wp/?p=36.

Will need to install gpiozero Python library if not already installed.

# How to use
On linux, cd to where you want to save prdpm and then run **python3 ./main.py** OR run **python3 /path/to/prdpm/main.py**.

Once running, prdpm will prompt you for a command. You can choose from the following:
```
o(n)     : Turn on device
o(ff)    : Turn off device
r(eset)  : Reset device
s(tatus) : Display device status (on/off)
h(elp)   : Display list of commands
e(xit)   : Exit Remote Device Power Management
```

Any input other than the above will give you the message "Command not supported. Type 'h(elp)' for list of commands."

# Individual Module Descriptions (incomplete)
## main.py
The menu where you input commands. See **How to use** for list of commands or type **h** or **help** in the menu.

## pwr_ctrl.py
The module that powers a device on and off.

Begins by assigning the **pwr** variable (see below). Then pings the device using the **target_host** variable (see below). Returns with a description of the device (on or off) and whether you want to power it on or off. Turning it on or off will set the GPIO pin state to HIGH for 0.5 seconds and then back to LOW which simulates pressing the power switch on a PC. Declining to turn the device on or off will take you back to the manin menu and a mistyped command will restart the module.

### pwr variable
The variable assigned to the GPIO pin connected to the ATX front panel power switch via the controller board. The gpiozero library uses Broadcom (BCM) pin numbering for the GPIO pins (see https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering); set to BCM pin 23 (i.e. board pin 16) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### target_host variable
The variable assigned to the IP address or hostname of target device. Used to tell whether the device is already on or off. Set to "freenas.local" by default; change this to the IP address or hostname of the device you want to power on or off.

## reset.py
The module that resets a device.

Works similarly to **pwr_ctrl.py**, but uses a different GPIO pin to reset a device and does so only if the device is on and you confirm the reset. Otherwise, it returns you to the main menu.

### pwr_rst variable
The variable assigned to the GPIO pin connected to the ATX front panel reset switch via the controller board. Set to BCM pin 27 (i.e. board pin 13) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### target_host variable
Same variable as the one used in **pwr_ctrl.py**.

## ping.py
The module that pings a device to find out if it is on or off.

Got this code from Google's Gemini AI overview because I'm unfamiliar with how Python's subprocess module works. Will attempt to rewrite it once I know more Python.

## status.py
The module that tells you whether a device is on or off using **ping.py**.

## help_rdpm.py
The module that lists all commands available in prdpm. See list in **How to use**.

## vars.py
The module that contains commonly used variables. Changes made here will apply to the entire program (e.g. changing target_host from "freenas.local" to "file-server.net" will change the device being pinged; Pi must be hooked up to the new device for prdpm to retain functionality).