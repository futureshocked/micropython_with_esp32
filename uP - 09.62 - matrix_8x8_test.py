'''
 09.62 - Use the 8x8 LED Matrix with the max7219 driver using SPI

 This sketch shows how to control the 8x8 LED Matrix to write text.


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


 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import max7219
from machine import Pin, SPI

#spi = SPI(2, baudrate=10000000, polarity=1, phase=0, sck=Pin(18), mosi=Pin(2))
spi = SPI(2, 10000000, sck=Pin(18), mosi=Pin(23))

ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 4)
display.fill(0)  # Fill screens white, all LEDs on
display.text('1234',0,0,1)  # Use LED off to write
display.brightness(5)
display.show()
