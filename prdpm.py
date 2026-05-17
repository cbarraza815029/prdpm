import os
import platform
import subprocess
from pathlib import Path
from time import sleep
import vars

#---------------------------------------------------------------------------------------------------
#Program Title Function
#---------------------------------------------------------------------------------------------------
#Prints the title of the program whenever it's called
def program_title():
    #clear_scren = "cls" if platform.system().lower() == "windows" else "clear"
    #os.system(clear_scren)
    print("---------------------------------------------------")
    print("Pi Remote Device Power Management Tool v2026.05.16")
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
#Pases through gpiozero pin for power or reset and "presses" it for 0.5 second
def push_button(select_pin):
    select_pin.on()
    sleep(0.5)
    select_pin.off()

#---------------------------------------------------------------------------------------------------
#Ping Function
#---------------------------------------------------------------------------------------------------
#Pings a network host and returns 0 (i.e. True) if the host responds, 1 (i.e. False) otherwise.
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
def status():
    program_title()
    print("Checking device status...")
    if ping(vars.target_host) == True:
        print(f"Host {vars.target_host} is on")
        print("")
    else:
        print(f"Host {vars.target_host} is off")
        print("")

#---------------------------------------------------------------------------------------------------
#On/Off Function
#---------------------------------------------------------------------------------------------------
#Submenu that uses the Ping function to check whether target device is reachable. If it is, 
#the On/Off function prompts the user if they would like to shutdown the device. If it is not
#reachable, the function asks if you would like to power on the device.
def on_off():
    program_title()
    if ping(vars.target_host) == True:
        print(f"{vars.target_host} is on")
        usr_input = input(f"Shutdown {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Shutting down {vars.target_host}...")
            push_button(vars.pwr)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Shutdown canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{vars.target_host} is off")
        usr_input = input(f"Power on {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Powering on {vars.target_host}...")
            push_button(vars.pwr)
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
def reset():
    program_title()
    if ping(vars.target_host):
        print(f"{vars.target_host} is on")
        usr_input = input(f"Reset {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Resetting {vars.target_host}...")
            push_button(vars.pwr_rst)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Reset canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{vars.target_host} is off")
        print("")

#---------------------------------------------------------------------------------------------------
#Change Function
#---------------------------------------------------------------------------------------------------
#Changes the saved hostname/ IP addrerss in vars.py of the target device.
def change_vars(file_param, new_target_host):
    with open(file_param, "r") as file:
        file_lines = file.readlines()
        for index, line in enumerate(file_lines, 1):
            if "target_host" in line:
                file_lines[index - 1] = f"{'target_host = "'}{new_target_host}{'"\n'}"
    with open(file_param, "w") as file:
        file.writelines(file_lines)

#---------------------------------------------------------------------------------------------------
#Change Sub Menu Function
#---------------------------------------------------------------------------------------------------
#Submenu for the above function.
def change_vars_sub_menu():
    program_title()
    file = "vars.py"
    file_dir = Path(__file__).parent.resolve()
    dir_slash = "\\" if platform.system().lower() == "windows" else "/"
    file_abs_path = f"{file_dir}{dir_slash}{file}"
    
    print(f"{'Current IP/ hostname: '}{vars.target_host}")
    usr_input = input("New IP/ hostname: ").strip()
    if usr_input == "exit" or usr_input == "e":
        print("Returning to main menu...")
        print("")
    else:
        change_vars(file_abs_path, usr_input)
        print(f"{'Success! IP address/ hostname changed from '}{'"'}{vars.target_host}{'"'}{' to '}{'"'}{usr_input}{'"'}")
        vars.target_host = usr_input
        print("")

#---------------------------------------------------------------------------------------------------
#Main Menu Function
#---------------------------------------------------------------------------------------------------
#Main menu of PRDPM.
def main():
    while True:
        program_title()
        usr_input = input("Command: ").lower().strip()
        print("")
        if usr_input == "on" or usr_input == "off" or usr_input == "o":
            on_off()
        elif usr_input == "reset" or usr_input == "r":
            reset()
        elif usr_input == "status" or usr_input == "s":
            status()
        elif usr_input == "change" or usr_input == "c":
            change_vars_sub_menu()
        elif usr_input == "help" or usr_input == "h":
            help()
        elif usr_input == "exit" or usr_input == "e":
            input("Press the 'Enter' key to exit...")
            break
        else:
            print("Command not supported. Type 'h(elp)' for list of commands.")
            print("")

main()