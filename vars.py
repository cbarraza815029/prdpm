from gpiozero import DigitalOutputDevice

pwr = DigitalOutputDevice(23)     # Variable for GPIO pin connected to ATX front panel power switch
pwr_rst = DigitalOutputDevice(27) # Variable for GPIO pin connected to ATX front panel reset switch
target_host = "freenas.local"     # Variable for IP address or hostname of controlled device