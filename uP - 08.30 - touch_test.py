'''
 08.30 - Internal touch sensor (Capacitive touch)

 This sketch shows how to use the ESP32 integrated capacitive touch sensor.
  
 Components
 ----------
  - ESP32
  - Connect a jumper wire to GPIO 15 (leave the other end unconnected)
  - Wires
  - Breadboard

 Documentation:
 Timers: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#timers
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 Touch: http://docs.micropython.org/en/latest/esp32/quickref.html#capacitive-touch
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import TouchPad, Pin
from time import sleep_ms

t = TouchPad(Pin(15))

while True:
    print(t.read())              # Returns a smaller number when touched
    sleep_ms(50)
    