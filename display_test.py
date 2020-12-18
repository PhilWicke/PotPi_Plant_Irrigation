import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import busio, digitalio, board, time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as RPIO

# Setting up RPIO for moisture sensors
RPIO.setmode(RPIO.BCM)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)

channel1 = AnalogIn(mcp, MCP.P0)
channel2 = AnalogIn(mcp, MCP.P1)


RST = None     # on the PiOLED this pin isnt used
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)


    RPIO.setup(18, RPIO.OUT)
    RPIO.setup(18, RPIO.LOW)  
    time.sleep(1)
    #print("Raw ADC Value: %.2f " % channel2.value)
    pot1_vol = "{0:.3f}V".format(channel1.voltage)
    #print("Raw ADC Value: %.2f " % channel1.value)
    pot2_vol = "{0:.3f}V".format(channel2.voltage)
    RPIO.setup(18, RPIO.HIGH)
    
    time.sleep(2)

    # Write two lines of text.

    draw.text((x, top),       "Pot 1 Volt.: " + str(pot1_vol),  font=font, fill=255)
    draw.text((x, top+8),     "Pot 2 Volt.: " + str(pot2_vol),  font=font, fill=255)
    #draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    #draw.text((x, top+25),    str(Disk),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)


