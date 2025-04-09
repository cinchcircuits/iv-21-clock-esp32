import board
import cp_mcp3x21
import time
import pwmio
import os
from max6921 import VFD
import digitalio
import supervisor

i2c = board.I2C()
mcp = cp_mcp3x21.MCP3021(i2c)

# This code is intended to test the DC 2 DC circuit before. 
# Ideally you verify the readings with a multimeter

# Initial startup values. Should make for a low voltage
#freq = 300
#freq = 14100
duty = 9000
vtarget = 27.0 # target voltage

# PWM on pin 7, duty cycle 0, 100khz
#pwm = pwmio.PWMOut(7, 0, 100000)
pwm = pwmio.PWMOut(board.D7, variable_frequency=True)
pwm.frequency = 3650
#pwm.frequency = 1050
pwm.duty_cycle = 0

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

# Used to reduce output of voltage updates
v_updates = 10

# Checks the VFS voltage. Adjust if nessary
def check_vfd(duty, updates):
    pwm.duty_cycle = duty
    #pwm.duty_cycle = 34000
    #pwm.duty_cycle = 40000
    lvoltage = get_voltage(mcp.value, 3.29, 1024)
    voltage = lvoltage * 17.75
    if voltage < vtarget:
        duty = duty+50
    else:
        duty = duty-50
    if duty > 63900:
        duty = 1000
    if updates == 1:    
        print(voltage)
        print(duty)
    return duty

while True:
    now_ms = supervisor.ticks_ms()
    div_ms = now_ms / 10
    div_sec = div_ms / 10
    if ( div_ms % 4 ) == 0:
        if v_updates >= 10:
            rduty = check_vfd(duty, 1)
            v_updates = 0
        else:
            rduty = check_vfd(duty, 0)
            v_updates = v_updates + 1
        duty = rduty


