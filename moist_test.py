from gpiozero import MCP3008
import time

ldr = MCP3008(channel=5)
ldb = MCP3008(channel=4)

while True:
    val1 = int((ldr.raw_value / 1023) * 1000)
    val2 = int((ldb.raw_value / 1023) * 1000)
    print("Value: ", val1, "|", val2)
    volt1 = ldr.voltage
    volt2 = ldb.voltage
    print("Volta: %.2f | %.2f" % (volt1, volt2))
    wert1 = int(ldr.value * 100)
    wert2 = int(ldb.value * 100)
    print("Perce: ", wert1, " | ", wert2)
    time.sleep(.5)
    print()