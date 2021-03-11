'''
 16.100 - Micro:bit integrated compass

 This script demonstrates how to use the Micro:bit on-board compass.

 The script reads the compass, prints out the heading and draws a line that points
 to the magnetic north on the LED integrated matrix display.


 Components
 ----------
  - Micro:bit

 Documentation:
 * Compass: https://microbit-micropython.readthedocs.io/en/v1.0.1/compass.html
 * Display: https://microbit-micropython.readthedocs.io/en/v1.0.1/display.html

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from microbit import *


# Start calibrating
#compass.calibrate()

# Try to keep the needle pointed in (roughly) the correct direction
while True:
    sleep(1)
    print(compass.heading())
    needle = ((15 - compass.heading()) // 30) % 12
    display.show(Image.ALL_CLOCKS[needle])
