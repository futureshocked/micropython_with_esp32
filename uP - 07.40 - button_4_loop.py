'''
 07.40 - Button state with loop

 This sketch shows how to read the state of a button using a "while" loop.
 When the button is pressed, the LED turns on for 10msec.

 Components
 ----------
  - ESP32
  - Momentary button with four pins
  -     These buttons usually come with four pins:
  -    1|     |4
  -     -------
  -     | / \ |
  -     | \ / |
  -     -------
  -    2|     |3
  -
  -     Connect pins 1 or 2 to GPIO4
  -     Connect pins 3 or 4 to GND
  -     No need for pull/up-down resistor (using internap pull-up)
  - 330Ohm resistor for the LED
  - 5mm LED
  -     Connect anode to GPIO 21
  -     Connect cathode to GND via the resistor
  - Wires
  - Breadboard

 Documentation:
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 sleep_ms: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep_ms
 ticks_ms: http://docs.micropython.org/en/latest/library/utime.html#utime.ticks_ms

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin
from utime import sleep_ms, ticks_ms

led = Pin(21, Pin.OUT)    # create output pin on GPIO21
button_pin4 = Pin(4, Pin.IN, Pin.PULL_UP)

while True:
    if button_pin4.value() == 0:
        led.on()
        print("Button pressed at ", ticks_ms())
        sleep_ms(10)
    else:
        led.off()
