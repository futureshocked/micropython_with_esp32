'''
 07.10 - LED blink with loop

 This sketch shows how to blink an LED connected to GPIO 21 using a loop.

 Components
 ----------
  - ESP32
  - 330Ohm resistor for the LED
  - 5mm LED
  -     Connect anode to GPIO 21
  -     Connect cathode to GND via the resistor
  - Wires
  - Breadboard

 Documentation:
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 sleep_ms: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep_ms

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin
from utime import sleep_ms # "utime" is an optimized subset version of the CPython time module

led = Pin(21, Pin.OUT)    # create output pin on GPIO21

while True:
    led.on()                 # set pin to "on" (high) level
    sleep_ms(500)
    led.off()                # set pin to "off" (low) level
    sleep_ms(500)

# You can also use:
# led.value(1)
# OR
# led.value(0)
