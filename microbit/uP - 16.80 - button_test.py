'''
 16.80 - Micro:bit with buttons

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

from microbit import *

while True:
    if button_a.is_pressed():
        display.show("A")
    elif button_b.is_pressed():
        display.show("B")
    else:
        display.show(Image.PACMAN)

display.clear()
