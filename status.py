import ping
    
def main():
    #print("Enter hostname or IP address")
    target_host = "freenas.local"
    print("Checking device status...")

    if ping.ping_host(target_host):
        print(f"Host {target_host} is on")
        print("")
    else:
        print(f"Host {target_host} is off")
        print("")
