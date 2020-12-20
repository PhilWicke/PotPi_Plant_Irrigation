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

def interpolate(val, source_range, target_range):
    a = source_range[0]
    b = source_range[1]
    c = target_range[0]
    d = target_range[1]
    
    return int(((1-((val-1)/(b-1)))*(c-d))+d)
    

# Setting up RPIO for moisture sensors
RPIO.setmode(RPIO.BCM)
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)

channel1 = AnalogIn(mcp, MCP.P0)
channel2 = AnalogIn(mcp, MCP.P1)

# Setting up OLED SPI pins
RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library and clear display
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image and clear with black box
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()

# Empirically determined wetness values
max_wet_pot1 = 1.8
min_wet_pot1 = 2.8

max_wet_pot2 = 0.7
min_wet_pot2 = 1.7

# Store data for plotting
current_sample_pot1 = []
current_sample_pot2 = []

# Starting Voltage scan
print("Start Voltage Scan")
RPIO.setup(18, RPIO.OUT)
RPIO.setup(18, RPIO.LOW)  
while True:
    try:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        #print("Raw ADC Value: %.2f " % channel2.value)
        volt_01 = channel1.voltage
        volt_02 = channel2.voltage
        
        pot1_vol = "{0:.3f}V".format(volt_01)
        #print("Raw ADC Value: %.2f " % channel1.value)
        pot2_vol = "{0:.3f}V".format(volt_02)
        
        pot1_volt= (volt_01 - min_wet_pot1) / (max_wet_pot1 - min_wet_pot1)
        pot1_perc = int(pot1_volt*100)
        pot1_perc_str = "{0:d}%".format(pot1_perc)
        pot2_volt= (volt_02 - min_wet_pot2) / (max_wet_pot2 - min_wet_pot2)
        pot2_perc = int(pot2_volt*100)
        pot2_perc_str = "{0:d}%".format(pot2_perc)
        
        # Set limit to 100%
        if pot1_perc>100:
            pot1_perc = 100
        if pot2_perc>100:
            pot2_perc =100
        
        # make it a fixed size by poping first element if too long 
        current_sample_pot1.append(pot1_perc)
        current_sample_pot2.append(pot2_perc)
        
        if len(current_sample_pot1) > ((width/2)-2):
            current_sample_pot1.pop(0)
            current_sample_pot2.pop(0)
        
        # Display Header Information
        draw.text((x, top),       "   Wetness of Soil",  font=font, fill=255)
        draw.text((x, top+8),     " Pot A:" + pot1_perc_str + "  Pot B:" + pot2_perc_str,  font=font, fill=255)
        
        # Draw Coordinate System - POT 1
        draw.line((x, top+20, x, top+height), fill=255, width=2)
        draw.line((x, top+height, x+(width/2)-2, top+height), fill=255, width=2)
        
        # Draw Coordinate System - POT 2
        draw.line((x+(width/2)+2, top+20, x+(width/2)+2, top+height), fill=255, width=2)
        draw.line((x+(width/2)+2, top+height, x+width, top+height), fill=255, width=2)
        
        # left first point at (0|0)
        # draw.point((x+2, top+63), fill=250)
        # left first point at (0|100)
        # draw.point((x+2, top+20), fill=250)
        
        # Plot data
        for idx, (point1, point2) in enumerate(zip(current_sample_pot1, current_sample_pot2)):
              pos_pix = interpolate(point1, [1,100], [height-1,20])
              draw.point((x+2+idx, top+pos_pix), fill=250)
              pos_pix = interpolate(point2, [1,100], [height-1,20])
              draw.point((x+(width/2)+2+idx, top+pos_pix), fill=250)
        
        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.05)
        
    except KeyboardInterrupt:
        print("Stopping Voltage Scan")
        RPIO.setup(18, RPIO.HIGH)
        disp.clear()
        disp.display()
        break



