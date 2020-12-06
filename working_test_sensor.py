import busio, digitalio, board, time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as RPIO

RPIO.setmode(RPIO.BCM)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)

channel1 = AnalogIn(mcp, MCP.P0)
channel2 = AnalogIn(mcp, MCP.P1)

while True:
    RPIO.setup(18, RPIO.OUT)
    RPIO.setup(18, RPIO.LOW)  
    time.sleep(1)
    #print("Raw ADC Value: %.2f " % channel2.value)
    print("1: ADC Voltage: %.2fV" % channel1.voltage)
    #print("Raw ADC Value: %.2f " % channel1.value)
    print("2: ADC Voltage: %.2fV" % channel2.voltage)
    RPIO.setup(18, RPIO.HIGH)
    
    time.sleep(2)
    
