import ping
import vars
import push

def on_off():
    if ping.ping_host(vars.target_host):
        print(f"{vars.target_host} is on")
        usr_input = input(f"Shutdown {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Shutting down {vars.target_host}...")
            push.button(vars.pwr)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Shutdown canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
    else:
        print(f"{vars.target_host} is off")
        usr_input = input(f"Power on {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Powering on {vars.target_host}...")
            push.button(vars.pwr)
            print("")
        elif usr_input == "n" or usr_input == "no":
            print("Power on canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
