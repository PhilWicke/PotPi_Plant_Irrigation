# PotPi - Pot Plant Irrigation System for Raspberry Pi 3

The irrigation system is build using a Raspberry Pi 3. The additional hardware:
 * 2x Capacitive Soil Moisture Sensors (analog)
 * 2x Mini Water pumps
 * 1x 0.96" I2C OLED Display
 * 1x 4 Channel 5V Relais 
 * 1x MPC3008 Analog to Digital Module
 * 1x Breadboard
 * 1x 9V Battery
 * Jumper Cables
 
The initial set for the main hardware was bought as a pack [here](https://www.amazon.de/gp/product/B07TJQSHR2). Since the moisture sensors are providing analog data, but the pi needs a digital signal, I also bough the MPC3008 module. Importantly, this code requires the [py-spidev library](https://github.com/doceme/py-spidev).
The script log humidity has been listed on crontab via "crontab -e":
37 13 * * * python3 /home/pi/Desktop/PotPi_Plant_Irrigation/log_humidity.py &
Doing so for a couple of days created the data in the log files to understand max and min moisure settings. This information has been incorporated in display_plot.py to display the moisture level of the two plots in real time on an OLED display (display_plot.py).
This is work in progress. For more information feel free to contact me.
