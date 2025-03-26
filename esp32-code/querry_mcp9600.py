import time
import board
import busio
import adafruit_mcp9600


i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
mcp = adafruit_mcp9600.MCP9600(i2c, 0x67)
mcpb = adafruit_mcp9600.MCP9600(i2c, 0x60)


while True:
    print((mcp.ambient_temperature, mcp.temperature, mcp.delta_temperature))
    print((mcpb.ambient_temperature, mcpb.temperature, mcpb.delta_temperature))
    print("")
    time.sleep(1)
