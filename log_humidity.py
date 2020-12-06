import busio, digitalio, board, time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime
import RPi.GPIO as RPIO
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, DateFormatter, DayLocator
        
# Setup RPIO channels
RPIO.setmode(RPIO.BCM)

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi,cs)

channel1 = AnalogIn(mcp, MCP.P0)
channel2 = AnalogIn(mcp, MCP.P1)

# Reset voltage three times
RPIO.setup(18, RPIO.OUT)
RPIO.setup(18, RPIO.LOW) # turn voltage on
time.sleep(1) # allow voltage to build
RPIO.setup(18, RPIO.HIGH) # turn voltage off
    

# Measure voltage 5 times and note average
measures_pot1 = []
measures_pot2 = []
for i in [1, 2, 3, 4, 5]:
    RPIO.setup(18, RPIO.OUT)
    RPIO.setup(18, RPIO.LOW)
    time.sleep(3)
    #print("Raw ADC Value: %.2f " % channel2.value)
    #print("1: ADC Voltage: %.2fV" % channel1.voltage)
    measures_pot1.append(channel1.voltage)
    measures_pot2.append(channel2.voltage)
    RPIO.setup(18, RPIO.HIGH)
    time.sleep(.5)

# Create time stamp and average values of sample 
date_time = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")
average_pot1 = sum(measures_pot1) / len(measures_pot1)
average_pot2 = sum(measures_pot2) / len(measures_pot2)

# Write last sample into log file
with open("/home/pi/Desktop/Pi_Plant_Irrigation/plant_log.txt", "a") as f_out:
    f_out.write("%s\tPot_1: %.3f V\tPot_2: %.3f V\n" % (date_time, average_pot1, average_pot2))
    
    
# Import all logs
log_dates = []
pot1_data = []
pot2_data = []
with open("/home/pi/Desktop/Pi_Plant_Irrigation/plant_log.txt", "r") as f_in:
    log_lines = f_in.readlines()
for line in log_lines:
    content = line.split("\t")
    date_info = content[0]
    pot1_val = content[1].split(" ")[1]
    pot2_val = content[2].split(" ")[1]
    
    log_dates.append(datetime.strptime(date_info, "%d.%m.%Y - %H:%M:%S"))
    pot1_data.append(float(pot1_val))
    pot2_data.append(float(pot2_val))
    
# Create new entries for log and plot
dates = date2num(log_dates)
plt.plot(log_dates, pot1_data, label="Pot 01")
plt.plot(log_dates, pot2_data, label="Pot 02")
plt.xlabel("Days")
plt.ylabel("Voltage (Humidity)")
plt.gca().xaxis.set_major_formatter(DateFormatter('%m-%d'))
plt.gca().xaxis.set_major_locator(DayLocator(interval=1))
plt.gca().xaxis.set_tick_params(rotation = 30)

# Save plot as png
plt.legend()
plt.savefig("/home/pi/Desktop/Pi_Plant_Irrigation/log_plot.png", format="png")
#plt.show()
