'''
 16.90 - Micro:bit integrated accelerometer and gestures

 This script demonstrates how to use the Micro:bit on-board accelerometer.

 The script reads the accelerometer every 0.a seconds and prints out the
 recognised gesture.


 Components
 ----------
  - Micro:bit

 Documentation:
 * Gestures: https://microbit-micropython.readthedocs.io/en/v1.0.1/tutorials/gestures.html


 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import utime
from microbit import *

while True:
    print(accelerometer.current_gesture())
    utime.sleep(0.1)
