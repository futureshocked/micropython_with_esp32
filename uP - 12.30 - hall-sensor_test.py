'''
 12.30 - Hall Sensor reading

 The ESP32 clock contains a Hall sensor which can be activated with a magnetic field.
 
 This script demonstrates how to read Hall sensor with the help of a small magnet.

  
 Components
 ----------
  - ESP32
  - A small magnet
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
    print(esp32.hall_sensor())
    sleep(0.1)
