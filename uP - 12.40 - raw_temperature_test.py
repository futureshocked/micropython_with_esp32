'''
 12.40 - Integrated raw temperature sensor reading

 The ESP32 clock contains a temperature sensor which can return readings in Farenheit.
 
 This script demonstrates how to read the integrated sensor.

  
 Components
 ----------
  - ESP32
  - Wires
  - Breadboard

 Documentation:
 Timers: http://docs.micropython.org/en/latest/esp32/quickref.html#timers
 Board control, frequency: http://docs.micropython.org/en/latest/esp32/quickref.html?highlight=osdebug#general-board-control
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import esp32
from time import sleep

while True:
    print("Raw temperature in Farenheit:", esp32.raw_temperature(), "°F")
    celsius = (esp32.raw_temperature() - 32)/1.8
    print("Raw temperature in Celsius:", round(celsius,2), "°C\n")
    sleep(1)
