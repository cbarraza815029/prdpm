import os
import platform
import subprocess
from pathlib import Path
from gpiozero import DigitalOutputDevice
from gpiozero.pins.rpigpio import RPiGPIOPin
from time import sleep
import json

#---------------------------------------------------------------------------------------------------
#Program Title Function
#---------------------------------------------------------------------------------------------------
#Prints the title of the program whenever it's called
def program_title():
    #clear_scren = "cls" if platform.system().lower() == "windows" else "clear"
    #os.system(clear_scren)
    print("---------------------------------------------------")
    print("Pi Remote Device Power Management Tool v2026.06.16")
    print("---------------------------------------------------")

#---------------------------------------------------------------------------------------------------
#Help Function
#---------------------------------------------------------------------------------------------------
#Prints list of available commands
def help():
    program_title()
    print("List of Commands:")
    print("o(n)     : Turn on device")
    print("o(ff)    : Turn off device")
    print("r(eset)  : Reset device")
    print("s(tatus) : Display device status (on/off)")
    print("c(hange) : Change IP address or hostname of device")
    print("h(elp)   : Display list of commands")
    print("e(xit)   : Exit Remote Device Power Management")
    print("")

#---------------------------------------------------------------------------------------------------
#Push Button Function
#---------------------------------------------------------------------------------------------------
#Pases through gpiozero pin for power or reset and "presses" it. Works by setting a GPIO pin state 
#to HIGH for 0.5 seconds and then back to LOW [i.e. vars.pwr.on(), sleep(0.5), vars.pwr.off()] 
#which simulates pressing the power switch on a PC.
def push_button(select_pin):
    select_pin.on()
    sleep(0.5)
    select_pin.off()

#---------------------------------------------------------------------------------------------------
#Ping Function
#---------------------------------------------------------------------------------------------------
#Pings a network host and returns 0 (i.e. True) if the host responds, 1 (i.e. False) otherwise.
#Sets the param variable to "-n" for windows systems or "-c" for linux systems and then 
#constructs the command variable using param and the device ip/hostname passed through 
#as a paramter from vars.py. Runs a subprocess the result of which gets assigned to the 
#ping_result variable. Finally, the returncode of ping_result gets compared to 0: 
#returns True if returncode equals 0 (i.e. success) otherwise returns False (i.e. failure).
def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ['ping', param, '1', host]
    ping_result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if ping_result.returncode == 0:
        return True
    else:
        return False

#---------------------------------------------------------------------------------------------------
#Status Function
#---------------------------------------------------------------------------------------------------
#Uses Ping function to check whether target device is reachable. Reachable = On while 
#Unreachable = Off or device still booting up (if previously powered/ reset)
def status(target_host_param):
    program_title()
    print("Checking device status...")
    if ping(target_host_param) == True:
        print(f"Host {target_host_param} is on")
        print("")
    else:
        print(f"Host {target_host_param} is off")
        print("")

#---------------------------------------------------------------------------------------------------
#On/Off Function
#---------------------------------------------------------------------------------------------------
#Submenu that uses the Ping function to check whether target device is reachable. If it is, 
#the On/Off function prompts the user if they would like to shutdown the device. If it is not
#reachable, the function asks if you would like to power on the device.
def on_off(target_host_param, dict_param):
    pwr = DigitalOutputDevice(dict_param["pwr"])

    program_title()
    if ping(target_host_param) == True:
        print(f"{target_host_param} is on")
        usr_input = input(f"Shutdown {target_host_param} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Shutting down {target_host_param}...")
            push_button(pwr)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Shutdown canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{target_host_param} is off")
        usr_input = input(f"Power on {target_host_param} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Powering on {target_host_param}...")
            push_button(pwr)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Power on canceled")
            print("")
        else:
            print("Command not supported")
            print("")

#---------------------------------------------------------------------------------------------------
#Reset Function
#---------------------------------------------------------------------------------------------------
#Submenu that uses the Ping function to check whether target device is reachable. If it is, 
#the Reset function prompts the user if they would like to reset the device. If it is 
#not reachable, the function returns to the manin menu.
def reset(target_host_param, dict_param):
    rst = DigitalOutputDevice(dict_param["pwr_rst"])

    program_title()
    if ping(target_host_param) == True:
        print(f"{target_host_param} is on")
        usr_input = input(f"Reset {target_host_param} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Resetting {target_host_param}...")
            push_button(rst)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Reset canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{target_host_param} is off")
        print("")

#---------------------------------------------------------------------------------------------------
#Change Function
#---------------------------------------------------------------------------------------------------
#Changes the saved hostname/ IP addrerss in vars.py of the target device. Imports the vars.py file 
#and usr_input var as parameters. Then opens vars.py and creates a list from its contents. The list 
#gets indexed and looks for the line of code containing "target_host" after which it gets changed 
#to the usr_input var. Completes the operation by writing the list back to vars.py.
def change_vars(file_param, dict_param, usr_input_ip_or_pin, usr_input_param):
    if type(usr_input_param) is str:
        dict_param["target_host"] = usr_input_param
    if type(usr_input_param) is int:
        if usr_input_ip_or_pin == "power" or usr_input_ip_or_pin == "pwr" or usr_input_ip_or_pin == "p":
            dict_param["pwr"] = usr_input_param
        if usr_input_ip_or_pin == "reset" or usr_input_ip_or_pin == "rst" or usr_input_ip_or_pin == "r":
            dict_param["pwr_rst"] = usr_input_param
    with open(file_param, 'w', encoding='utf-8') as file:
            json.dump(dict_param, file, ensure_ascii=False)
    return dict_param

#---------------------------------------------------------------------------------------------------
#Check Input Error Function
#---------------------------------------------------------------------------------------------------
#Checks for value errors in user input when changing power or reset pins
def check_input_error(pin_pwr_or_rst, pwr_pin, rst_pin):
    valid_gpio_pins = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    if pin_pwr_or_rst == "power" or pin_pwr_or_rst == "pwr" or pin_pwr_or_rst == "p":
        pin_type = "power"
    if pin_pwr_or_rst == "reset" or pin_pwr_or_rst == "rst" or pin_pwr_or_rst == "r":
        pin_type = "reset"
    pin_final_val = None
    while pin_final_val is None:
        try:
            pin_final_val = int(input(f"New {pin_type} pin: ").lower().strip())
        except ValueError:
            print("Integer values only. Please try again!")
    if pin_final_val not in valid_gpio_pins:
        print(f"Error: Pin {pin_final_val} is not a valid BCM numbered GPIO pin. Please try again!")
        check_input_error(pin_type, pwr_pin, rst_pin)
    if pin_final_val == pwr_pin and pin_type == "reset":
        print(f"Error: Pin {pin_final_val} currently in use by the power pin. Please try again!")
        check_input_error(pin_type, pwr_pin, rst_pin)
    if pin_final_val == rst_pin and pin_type == "power":
        print(f"Error: Pin {pin_final_val} currently in use by the reset pin. Please try again!")
        check_input_error(pin_type, pwr_pin, rst_pin)
    else:
        return pin_final_val

#---------------------------------------------------------------------------------------------------
#Change Sub Menu Function
#---------------------------------------------------------------------------------------------------
#Submenu for the above function. Begins by creating the file_abs_path variable that stores the 
#location of the vars.py file as a string. Then it prints the current ip/hostname and prompts 
#you for a new one. Entering "exit" or "e" will return you to the main menu. Anything else will
#run the change_vars function that changes the target_host variable in the vars.py file. It 
#completes by printing a success message and changes the target_host var in memory so you don't 
#need to restart prdpm for the ip/hostname change to take effect.
def change_vars_sub_menu(file_path_param, dict_param_change_menu, target_host_param):
    program_title()
    pwr = dict_param_change_menu["pwr"]
    pwr_rst = dict_param_change_menu["pwr_rst"]
    while True:
        usr_input_init = input("Change IP/ hostname or pins?: ").strip().lower()
        if usr_input_init == "ip" or usr_input_init == "i" or usr_input_init == "hostname" or usr_input_init == "host" or usr_input_init == "name" or usr_input_init == "h":
            print(f"{'Current IP/ hostname: '}{target_host_param}")
            usr_input_ip = input("New IP/ hostname: ").strip()
            sett_dict = change_vars(file_path_param, dict_param_change_menu, usr_input_init, usr_input_ip)
            #print(f"{'Success! IP address/ hostname changed from '}{'"'}{target_host}{'"'}{' to '}{'"'}{usr_input_ip}{'"'}")
            return sett_dict
        if usr_input_init == "pins" or usr_input_init == "pin" or usr_input_init == "p":
            usr_input_pin_sel = input("Change power or reset pin?: ").strip().lower()
            if usr_input_pin_sel == "power" or usr_input_pin_sel == "pwr" or usr_input_pin_sel == "p":
                print(f"{'Current power pin: '}{pwr}")
                usr_input_pin_pwr = check_input_error(usr_input_pin_sel, pwr, pwr_rst)
                sett_dict = change_vars(file_path_param, dict_param_change_menu, usr_input_pin_sel, usr_input_pin_pwr)
                #print(f"{'Success! Power pin changed from '}{'"'}{pwr}{'"'}{' to '}{'"'}{usr_input_ip}{'"'}")
                return sett_dict
            if usr_input_pin_sel == "reset" or usr_input_pin_sel == "rst" or usr_input_pin_sel == "r":
                print(f"{'Current reset pin: '}{pwr_rst}")
                usr_input_pin_rst = check_input_error(usr_input_pin_sel, pwr, pwr_rst)
                sett_dict = change_vars(file_path_param, dict_param_change_menu, usr_input_pin_sel, usr_input_pin_rst)
                return sett_dict
        if usr_input_init == "exit" or usr_input_init == "e" or usr_input_init == "back" or usr_input_init == "b" or usr_input_init == "return" or usr_input_init == "rtrn":
            print("Returning to main menu...")
            print("")
            break
        else:
            print("Command not supported. Type 'h(elp)' for list of commands.")
            print("")

#---------------------------------------------------------------------------------------------------
#Main Menu Function
#---------------------------------------------------------------------------------------------------
#Main menu of prdpm.
def main():
    file = "settings.json"
    file_dir = Path(__file__).parent.resolve()
    dir_slash = "\\" if platform.system().lower() == "windows" else "/"
    file_abs_path = f"{file_dir}{dir_slash}{file}"

    if Path(file_abs_path).is_file():
        pass
    else:
        Path(file_abs_path).touch(exist_ok=True)
        default_settings = {
            "pwr": 23,
            "pwr_rst": 27,
            "target_host": "freenas.local"
        }
        with open(file_abs_path, 'w', encoding='utf-8') as file:
            json.dump(default_settings, file, ensure_ascii=False)

    with open(file_abs_path, 'r', encoding='utf-8') as settings_read_file:
        settings_dict = json.load(settings_read_file)
    
    while True:
        target_host = settings_dict["target_host"]
        
        program_title()
        usr_input = input("Command: ").lower().strip()
        print("")
        if usr_input == "on" or usr_input == "off" or usr_input == "o":
            on_off(target_host, settings_dict)
        elif usr_input == "reset" or usr_input == "r":
            reset(target_host, settings_dict)
        elif usr_input == "status" or usr_input == "s":
            status(target_host)
        elif usr_input == "change" or usr_input == "c":
            settings_dict = change_vars_sub_menu(file_abs_path, settings_dict, target_host)
        elif usr_input == "help" or usr_input == "h":
            help()
        elif usr_input == "exit" or usr_input == "e":
            input("Press the 'Enter' key to exit...")
            break
        else:
            print("Command not supported. Type 'h(elp)' for list of commands.")
            print("")
main()