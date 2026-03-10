# Description
Pi Remote Device Power Management Tool (prdpm) is a python script intended to run on Raspberry Pi SBCs equipped with a 40-pin GPIO header.

This project was designed to control a single device with a Pi via an ATX Controller board. Any board should work although you will need to make modifications to the code if you're not using the controller board from https://perdeas.com/wp/?p=36.

You will need to install the following Python libraries to get prdpm working: gpiozero, lgpio, and rpi.gpio. These come pre-installed in Raspberry Pi OS if you're running that already.

# How to use
On linux, cd to where you want to clone prdpm and then run **python3 ./main.py** OR run **python3 /path/to/prdpm/main.py**.

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
## main.py
The menu where you input commands. See **How to use** for list of commands or type **h** or **help** in the menu.

## vars.py
The module that contains commonly used variables. Changes made here will apply to the entire program (e.g. changing target_host from "freenas.local" to "file-server.net" will change the device being pinged; Pi must be hooked up to the new device for prdpm to continue working). The variables are:

### pwr variable
The variable assigned to the GPIO pin connected to the ATX front panel power switch via the controller board. The gpiozero library uses Broadcom (BCM) pin numbering for the GPIO pins (see https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering); set to BCM pin 23 (i.e. board pin 16) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### pwr_rst variable
The variable assigned to the GPIO pin connected to the ATX front panel reset switch via the controller board. Set to BCM pin 27 (i.e. board pin 13) by default for use with the perdeas controller board. You can change this to a different pin if using a different controller board.

### target_host variable
The variable assigned to the IP address or hostname of target device. Used to tell whether the device is already on or off. Set to "freenas.local" by default; change this to the IP address or hostname of the device you want to power on or off.

## push.py
The module that powers a device on and off.

Works by setting a GPIO pin state to HIGH for 0.5 seconds and then back to LOW [i.e. vars.pwr.on(), sleep(0.5), vars.pwr.off()] which simulates pressing the power switch on a PC. The GPIO pin gets passed through as a parameter so this module can be utitlized by both **pwr_ctrl.py** and **reset.py**.

## pwr_ctrl.py
The module that controls whether a device gets powered on or off.

Begins by pinging the device using the **target_host** variable (see vars.py). Returns with a description of the device (on or off) and whether you want to power it on/off. Accepting will turn the device on/off while declining will take you back to the main menu. For example, prdpm displays that freenas.local is off and asks you if you'd like to power it on. Typing y/yes will turn it on while typing n/no will take you back to the main menu. A mistyped command will give you the message "Command not supported" and restart the module.

Uses the **pwr** and **target_host** variables.

## reset.py
The module that resets a device.

Works similarly to **pwr_ctrl.py**, but uses a different GPIO pin to reset a device and does so only if the device is on and you confirm the reset. Otherwise, it returns you to the main menu.

Uses the **pwr_rst** and **target_host** variables.

## ping.py
The module that pings a device to find out if it is on or off.

Sets the **param** variable to "-c" for linux systems (can comment it out and uncomment the "-n" param var for windows systems). Then constructs the **command** variable using **param** and the device ip/hostname passed through as a paramter from **vars.py**. Runs a subprocess the result of which gets assigned to the **ping_result** variable. Finally, the returncode of **ping_result** gets compared to 0: returns True if returncode equals 0 (i.e. success) otherwise returns False (i.e. failure).

## status.py
The module that tells you whether a device is on or off using **ping.py**.

Uses the **target_host** variable.

## change.py
The module that controls the ip/hostname of the controlled device.

Begins by creating the **file_abs_path** variable that stores the location of the **vars.py** file as a string. Then it prints the current ip/hostname and prompts you for a new one. Entering "exit" or "e" will return you to the main menu. Anything else will run the **ip_host.py** module that changes the **target_host** variable in the **vars.py** file. It completes by printing a success message and changes the **target_host** var in memory so you don't need to restart prdpm for the ip/hostname change to take effect.

## ip_host.py
The module that changes the ip/hostname of the controlled device.

Imports the **vars.py** file, **target_host** var, and **usr_input** var (from **change.py**) as parameters. Then opens **vars.py** and creates a list from its contents. The list gets indexed and looks for the line of code containing "target_host" after which it gets changed to the **usr_input** var. Completes the operation by writing the list back to **vars.py**.

## help_rdpm.py
The module that lists all commands available in prdpm. See list in **How to use**.