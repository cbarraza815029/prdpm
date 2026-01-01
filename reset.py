from gpiozero import DigitalOutputDevice
from time import sleep
import ping

pwr_rst = DigitalOutputDevice(27)

def reset():
    target_host = "freenas.local"

    if ping.ping_host(target_host):
        print(f"{target_host} is on")
        print(f"Reset {target_host} (y/n)?")
        usr_input = input(":~ $ ").lower().strip()
        if usr_input == "y":
            print(f"Resetting {target_host}...")
            pwr_rst.on()
            sleep(0.5)
            pwr_rst.off()
            print("")
        elif usr_input == "n":
            print("Reset canceled")
            print("")
        else:
            print("Command not supported")
            print("")
    else:
        print(f"{target_host} is off")
        print("")
