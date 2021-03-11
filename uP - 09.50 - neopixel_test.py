'''
 09.50 - Use the Neopixel addressable RGB LEDs

 This sketch shows how to control the individual RGB LEDs in a strip of Neopixels. 
 
  
 Components
 ----------
  - ESP32
  - A Neopixels strip with 8 RGB LEDs
  -     GND --> GND
  -     VCC --> 5V
  -     DIN --> GPIO 13
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * Neopixel driver: https://docs.micropython.org/en/latest/esp32/quickref.html#neopixel-driver
 
 Beware:
 The ESP32 micropython firmware includes the Neopixels drivers. There is nothing else to install.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from random import *

pin = Pin(13, Pin.OUT)   # set GPIO13 to output to drive NeoPixels
np = NeoPixel(pin, 8)   # create NeoPixel driver on GPIO0 for 8 pixels

# You can control the color of each pixel by storing an RGB value for each one.
# I have commented out the following lines because I am using a loop to
# write random colors to each pixel.
#np[0] = (0, 0, 200) # set the first pixel to white
#np[1] = (200, 0, 0)
#np[2] = (0, 255, 0)
#np[3] = (100, 255, 0)
#np[4] = (100, 255, 50)
#np[5] = (0, 120, 100)
#np[6] = (100, 200, 0)
#np[7] = (100, 0, 50)
#np.write()              # write data to all pixels
#r, g, b = np[0]         # get first pixel colour

while True:
    for x in range(8):
        np[x] = (randint(0, 10), randint(0, 10), randint(0, 10))  # Keeping the brightness low to prevent blindness
    
    np.write()
    sleep_ms(60)
    for x in range(8):
        np[x] = (0, 0, 0)
    
    np.write()    
    sleep_ms(15)
