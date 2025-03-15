# SPDX-FileCopyrightText: 2021 Andon
#
# SPDX-License-Identifier: MIT

"""
'MCP3X21'
==========================================

CircuitPython module for the MCP3021 and MCP3221 ADCs.
The MCP3021 is a 10-bit, while the MCP3221 is 12-bit.
Both are otherwise the same: I2C devices with a single
analog input.

* Author(s): Andon (2021)
"""

__version__ = "0.1.0"
__repo__ = "(To Be Determined)"

from micropython import const
from adafruit_bus_device import i2c_device

# The address differs depending on which chip is used.
# These addresses are for both the 3021 and 3221
# A0T = 0x48
# A1T = 0x49
# A2T = 0x4a
# A3T = 0x4b
# A4T = 0x4c
# A5T = 0x4d (Default)
# A6T = 0x4e
# A7T = 0x4f
# The A5T is what the manufacturer says is default,
# So use it as default.
_ADDRESS = const(0x4e)

class MCP3X21:
    """ Supports the MCP3021 and MCP3221.
    I don't have an MCP3221 to test, but they look to
    be more or less the same.
    """
    def __init__(self, bus_device, address=_ADDRESS):
        self._device = i2c_device.I2CDevice(bus_device, address)
    
    def _read(self, bits):
        # Reads the value of the device.
        # These things are super simple.
        with self._device as bus_device:
            _BUFFER = bytearray(2)
            bus_device.readinto(_BUFFER)
            if bits == 10:
                # 10-bit device.
                return (_BUFFER[0] << 6) | _BUFFER[1] >> 2
            elif bits == 12:
                # 12-bit device.
                return (_BUFFER[0] << 8) | _BUFFER[1]
            else:
                raise ValueError("Only the MCP3021 and MCP3221 are supported.")

class MCP3021(MCP3X21):
    # Class for the MCP3021, a 10-bit device.
    
    @property
    def value(self):
        return self._read(10)

class MCP3221(MCP3X21):
    # Class for the MCP3221, a 12-bit device.
    
    @property
    def value(self):
        return self._read(12)

