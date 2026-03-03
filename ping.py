import subprocess

#Pings a network host and returns 0 (i.e. True) if the host responds, 1 (i.e. False) otherwise.
def ping_host(host):
    param = '-c' #For Linux systems
    #param = '-n' #For Windows systems
    
    command = ['ping', param, '1', host]

    ping_result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if ping_result.returncode == 0:
        return True
    else:
        return False