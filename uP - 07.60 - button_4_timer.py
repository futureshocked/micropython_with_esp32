'''
 07.60 - Button state with hardware timer.

 This sketch shows how to read the state of a button using a hardware timer
 instead of a "while" loop.

 When the button is pressed, the LED turns on for 1 sec.

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
 disable_irq: http://docs.micropython.org/en/latest/library/machine.html#machine.disable_irq
 enable_irq: http://docs.micropython.org/en/latest/library/machine.html#machine.enable_irq


 Beware:
 The IRQ must be dissabled for a very short abount of time.
 If not, the watch dog will reboot the device.

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, Timer
from time import sleep_ms

led = Pin(21, Pin.OUT)    # create output pin on GPIO21

button_pin4 = Pin(4, Pin.IN, Pin.PULL_UP)

button_pressed = False

def button_pressed_isr(event):
    global button_pressed
    global button_event

    if button_pin4.value() == False:
        button_pressed = True
        button_event = event
    else:
        button_pressed = False


button_timer = Timer(1)
button_timer.init(period=50, mode=Timer.PERIODIC, callback=button_pressed_isr)

while True:
    if button_pressed == True:
        button_pressed = False
        led.on()
        print("Button pressed event", button_event)
        sleep_ms(1000)
    else:
        led.off()
