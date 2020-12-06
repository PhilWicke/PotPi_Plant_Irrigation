import RPi.GPIO as RPIO
import time


RPIO.setmode(RPIO.BCM)

pump_1 = 3
pump_2 = 17


RPIO.setup(pump_1, RPIO.OUT)
RPIO.setup(pump_1, RPIO.LOW)
time.sleep(0.75)
RPIO.setup(pump_1, RPIO.HIGH)

time.sleep(.5)
RPIO.setup(pump_2, RPIO.OUT)
RPIO.setup(pump_2, RPIO.LOW)
time.sleep(0.75)
RPIO.setup(pump_2, RPIO.HIGH)



