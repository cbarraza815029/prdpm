import pwr_ctrl
import reset
import status
import ping
import help_rdpm
import change

def main():
    print("---------------------------------------------------")
    print("Pi Remote Device Power Management Tool v2026.03.09")
    print("---------------------------------------------------")
    usr_input = input("Command: ").lower().strip()
    if usr_input == "on" or usr_input == "off" or usr_input == "o":
        pwr_ctrl.on_off()
        main()
    elif usr_input == "reset" or usr_input == "r":
        reset.reset()
        main()
    elif usr_input == "status" or usr_input == "s":
        status.main()
        main()
    elif usr_input == "change" or usr_input == "c":
        change.main()
        main()
    elif usr_input == "help" or usr_input == "h":
        help_rdpm.help()
        main()
    elif usr_input == "exit" or usr_input == "e":
        input("Press the 'Enter' key to exit...")
        exit
    else:
        print("Command not supported. Type 'h(elp)' for list of commands.")
        print("")
        main()
main()