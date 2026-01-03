from time import sleep
import ping
import vars

def on_off():
    if ping.ping_host(vars.target_host):
        print(f"{vars.target_host} is on")
        print(f"Shutdown {vars.target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Shutting down {vars.target_host}...")
            vars.pwr.on()
            sleep(0.5)
            vars.pwr.off()
            print("")
        elif usr_input == "n":
            print("Shutdown canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
    else:
        print(f"{vars.target_host} is off")
        print(f"Power on {vars.target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Powering on {vars.target_host}...")
            vars.pwr.on()
            sleep(0.5)
            vars.pwr.off()
            print("")
        elif usr_input == "n":
            print("Power on canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
