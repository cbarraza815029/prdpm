from gpiozero import DigitalOutputDevice
from time import sleep
import ping

pwr = DigitalOutputDevice(23)

def on_off():
    target_host = "freenas.local"

    if ping.ping_host(target_host):
        print(f"{target_host} is on")
        print(f"Shutdown {target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Shutting down {target_host}...")
            pwr.on()
            sleep(0.5)
            pwr.off()
            print("")
        elif usr_input == "n":
            print("Shutdown canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
    else:
        print(f"{target_host} is off")
        print(f"Power on {target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Powering on {target_host}...")
            pwr.on()
            sleep(0.5)
            pwr.off()
            print("")
        elif usr_input == "n":
            print("Power on canceled")
            print("")
        else:
            print("Command not supported")
            print("")
            on_off()
