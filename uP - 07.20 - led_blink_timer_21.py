'''
 07.20 - LED blink with timer

 This sketch shows how to blink an LED connected to GPIO 21 using a timer instead of a loop.

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
 Timers: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#timers
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, Timer

led = Pin(21, Pin.OUT)    # create output pin on GPIO21

def blink_isr(event):
    if led.value() == False:
        led.on()
    else:
        led.off()

blink_timer = Timer(1)
blink_timer.init(period=250, mode=Timer.PERIODIC, callback=blink_isr)
