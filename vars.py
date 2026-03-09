from gpiozero import DigitalOutputDevice

# Variable for GPIO pin connected to ATX front panel power switch
pwr = DigitalOutputDevice(23)

# Variable for GPIO pin connected to ATX front panel reset switch
pwr_rst = DigitalOutputDevice(27)

# Variable for IP address or hostname of controlled device
target_host = "freenas.local"