import ping
import vars

def main():
    print("Checking device status...")
    if ping.ping_host(vars.target_host):
        print(f"Host {vars.target_host} is on")
        print("")
    else:
        print(f"Host {vars.target_host} is off")
        print("")
