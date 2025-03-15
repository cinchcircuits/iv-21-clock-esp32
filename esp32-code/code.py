import board
import cp_mcp3x21
import time
import pwmio
import adafruit_ntp
import socketpool
import wifi
import os
from max6921 import VFD
import digitalio

i2c = board.I2C()
mcp = cp_mcp3x21.MCP3021(i2c)

# Filament transistor attached to pin 2
#fpwm = pwmio.PWMOut(board.D2, variable_frequency=True)
#fpwm.frequency = 200
#pwm.frequency = 1050
#fpwm.duty_cycle = 1000

# PWM on pin 7, duty cycle 0, 100khz
#pwm = pwmio.PWMOut(7, 0, 100000)
pwm = pwmio.PWMOut(board.D7, variable_frequency=True)
pwm.frequency = 34050
#pwm.frequency = 1050
pwm.duty_cycle = 0

freq = 4100
#freq = 14100
duty = 12000
vtarget = 27.0 # target voltage

# Get wifi AP credentials from a settings.toml file
wifi_ssid = os.getenv("CIRCUITPY_WIFI_SSID")
wifi_password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
if wifi_ssid is None:
    print("WiFi credentials are kept in settings.toml, please add them there!")
    raise ValueError("SSID not found in environment variables")

try:
    print("Attempting wifi connection")
    wifi.radio.connect(wifi_ssid, wifi_password)
except ConnectionError:
    print("Failed to connect to WiFi with provided credentials")
    raise

timez = os.getenv("TIMEZONE")
timezone = int(timez)

pool = socketpool.SocketPool(wifi.radio)
ntp = adafruit_ntp.NTP(pool, tz_offset=timezone, cache_seconds=3600)

print(ntp.datetime)

load = digitalio.DigitalInOut(board.D3)
load.direction = digitalio.Direction.OUTPUT
digits = [(load, 15), (load, 1), (load, 13), (load, 2), (load, 14), (load, 0), (load, 12), (load, 11),(load, 10), (load, 17), (load, 18), (load, 19)]
segments = [(load, 7), (load, 8), (load, 9), (load, 16), (load, 4), (load, 3), (load, 5), (load, 6)]

vfd = VFD(digits, segments)

vfd.print("012")
vfd.draw()

def get_voltage(value, ref, max_value=1024):
    # Our value will be between 0 and either 1024 or 4096, depending.
    # We'll default to the max being 1024, but that can be changed.
    value = float(value) # We want the final result to be a float anyway.
    # What we do here is take the proportion of the value to the max value
    # And multiply that by the voltage we're measuring.
    # So if we have a lipo battery that tops out at 4.2v, we'd use 4.2 as
    # the reference. If our reading is 900 out of 1024, that's 0.88 (ish),
    # multiplied by 4.2 gives us 3.7v, or a usual battery charge. If it was
    # around 780, that'd be at 3.2 volts, or worryingly dead.
    volts = (value / max_value) * ref
    return volts

#vs = 10.0
time.sleep(5)
pwm.duty_cycle = duty
pwm.frequency = freq
print("duty")
print(duty)
print("freq")
print(freq)

# start Filament F2
filament = digitalio.DigitalInOut(board.D2)
filament.direction = digitalio.Direction.OUTPUT
filament.value = True

while True:
	#print(mcp.value)
	#time.sleep(0.1)
	pwm.duty_cycle = duty
	#pwm.duty_cycle = 34000
	#pwm.duty_cycle = 40000
	lvoltage = get_voltage(mcp.value, 3.29, 1024)
	voltage = lvoltage * 17.75
	print(voltage)
	if voltage < vtarget:
		duty = duty+50
	else:
		duty = duty-50
	if duty > 63900:
		duty = 50
	print(duty)
	#if voltage < vtarget:
	#	freq = freq + 50
	#else:
	#	freq = freq - 50
	#print(freq)
	#pwm.frequency = freq
	#vfd.print("01234567")
	vfd.print("76543210")
	vfd.draw()


