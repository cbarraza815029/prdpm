#Got code below from Google Gemini AI overview
import subprocess
import platform

def ping_host(host):
    """
    Pings a network host and returns True if the host responds, False otherwise.
    """
    # Determine the correct ping command parameter based on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Construct the ping command
    # -c 1 or -n 1 sends a single ping packet
    command = ['ping', param, '1', host]

    # Execute the command and capture the return code
    # A return code of 0 typically indicates success
    try:
        return subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
    except FileNotFoundError:
        print("Error: 'ping' command not found. Ensure it's in your system's PATH.")
        return False
