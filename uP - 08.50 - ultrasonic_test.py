'''
 08.50 - Ultrasonic distance sensor, HC-SR04

 This sketch shows how to use the ESP32 HC-SR04 ultrasonic distance sensor.
  
 Components
 ----------
  - ESP32
  - HC-SR04 sensor, with these connections:
  -     Grnd --> GND
  -     Echo --> GPIO 15
  -     Trig --> GPIO 2
  -     Vcc  --> 3.3V
  - Wires
  - Breadboard

 Documentation:
 Timers: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#timers
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 HC-SR04 driver source: https://github.com/rsc1975/micropython-hcsr04
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, Timer
from hc_sr04 import HCSR04

sensor = HCSR04(trigger_pin=2, echo_pin=15,echo_timeout_us=1000000)

def hcrs04_isr(event): 
    distance = sensor.distance_cm()
    print(distance)
    
blink_timer = Timer(1)
blink_timer.init(period=250, mode=Timer.PERIODIC, callback=hcrs04_isr)
