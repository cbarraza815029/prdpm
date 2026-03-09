import ping
import vars
import push

def reset():
    if ping.ping_host(vars.target_host):
        print(f"{vars.target_host} is on")
        usr_input = input(f"Reset {vars.target_host} (y/n)?: ").lower().strip()
        if usr_input == "y" or usr_input == "yes":
            print(f"Resetting {vars.target_host}...")
            push.button(vars.pwr_rst)
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
