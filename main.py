import pwr_ctrl
import reset
import status
import ping
import help_rdpm

def main():
    print("---------------------------------------------------")
    print("Pi Remote Device Power Management Tool v2025.12.13")
    print("---------------------------------------------------")
    print("Enter Command")
    usr_input = input(":~ $ ").lower().strip()
    if usr_input == "on":
        pwr_ctrl.on_off()
        main()
    elif usr_input == "off":
        pwr_ctrl.on_off()
        main()
    elif usr_input == "reset":
        reset.reset()
        main()
    elif usr_input == "status":
        status.main()
        main()
    elif usr_input == "help":
        help_rdpm.help()
        main()
    elif usr_input == "exit":
        input("Press the 'Enter' key to exit...")
        exit
    else:
        print("Command not supported. Type 'help' for list of commands.")
        print("")
        main()
main()
