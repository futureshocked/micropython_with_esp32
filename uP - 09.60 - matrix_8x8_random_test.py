'''
 09.60 - Use the 8x8 LED Matrix with the max7219 driver using SPI

 This sketch shows how to control the 8x8 LED Matrix to draw random pixels.


 Components
 ----------
  - ESP32
  - One or more 8x8 LED matrix displays with the max7219 driver
  -     GND --> GND
  -     VCC --> 5V
  -     CS  --> GPIO 5  (SPI SS)
  -     CLK --> GPIO 18 (SPI SCK)
  -     DIN --> GPIO 23 (SPI MOSI)
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * SPI (hardware): https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-spi-bus
 * max7219: https://github.com/mcauser/micropython-max7219
 * random function: https://docs.python.org/3/library/random.html

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import max7219
from machine import Pin, SPI
from utime import sleep_ms
from random import *

#spi = SPI(2, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(23))
spi = SPI(2, 10000000, sck=Pin(18), mosi=Pin(23))

ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 4)
display.fill(0)
display.brightness(5)

while True:
    for x in range(10):
        display.pixel(randint(0, 31), randint(0, 7),1)
    display.show()
    sleep_ms(15)
    display.fill(0)
