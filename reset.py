from time import sleep
import ping
import vars

def reset():
    if ping.ping_host(vars.target_host):
        print(f"{vars.target_host} is on")
        print(f"Reset {vars.target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Resetting {vars.target_host}...")
            vars.pwr_rst.on()
            sleep(0.5)
            vars.pwr_rst.off()
            print("")
        elif usr_input == "n":
            print("Reset canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{vars.target_host} is off")
        print("")
