'''
 16.70 - Micro:bit with Neopixels

 This script demonstrates how to drive a small Neopixel bar with a
 Micro:bit and MicroPython.

 Beware: the Neopixel normally requires 5V for full brightness. If you are only
 using up to 2 or 3 of the pixels, you can safely power it with 3.3V from the
 Micro:bit.


 Components
 ----------
  - Micro:bit
  - Micro:bit breadboard breakout
  - Neopixel bar with 8 Neopixels
  -   Vcc to 3.3V
  -   GND to GND
  -   DIN to P0
  - Wires
  - Breadboard

 Documentation:
 * Neopixels: https://microbit-micropython.readthedocs.io/en/v1.0.1/neopixel.html


 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import neopixel
from microbit import *
import utime

np = neopixel.NeoPixel(pin0, 8)

while True:
    for x in range(8):
        #print(x)
        np.clear()
        np[x] = (100,0,0)
        np.show()
        utime.sleep(0.1)

    #print("Down")

    for x in range(7,-1,-1):
        #print(x)
        np.clear()
        np[x] = (0,100,0)
        np.show()
        utime.sleep(0.1)

    #print("Upc")
