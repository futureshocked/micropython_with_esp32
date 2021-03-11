'''
 10.20 - Control a 5 Volt motor with the DRV8871 controller

 This sketch shows how to control a 5 Volt motor using the DRV8871 controller.
 
 You can use this sketch with other motor controllers that rely on PWM for speed control.
 
  
 Components
 ----------
  - ESP32
  - 5V motor
  - DRV8871 motor controller
  -     GND    --> GND
  -     IN1  --> GPIO21  (controls direction)
  -     IN2  --> GPIO2 (controls speed via PWM)
  -     VM   --> Not connected (controller is powered by the motor power source)
  -     Power+ --> Power source 6.5V
  -     Power- --> Power source - or GND
  -     Motor 1 --> motor wire 1
  -     Motor 2 --> motor wire 2
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * PWM: http://docs.micropython.org/en/latest/esp32/quickref.html#pwm-pulse-width-modulation
 * DRV8871 from Adafruit: https://learn.adafruit.com/adafruit-drv8871-brushed-dc-motor-driver-breakout
 
 Beware:
 The DRV8871 has a minimum of 6.5V input power for the motor. If you supply a smaller voltage,
 the motor will not work.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, PWM
from utime import sleep

in2 = PWM(Pin(2))     # Speed
in1 = Pin(21, Pin.OUT)  # Direction

in2.freq(500)         # set frequency. 1000 is default

while True:
    # Forward
    # in2:  1023 <-- Slower - Faster --> 0
    in1.on()
    print("Forward")
    in2.duty(0)  # Fast
    sleep(1)
    in2.duty(100)  # Slow
    sleep(1)
    in2.duty(200)  # Slower
    sleep(1)
    in2.duty(300)  # Slower x 2
    sleep(1)
    in2.duty(1023)  # stop
    sleep(1)

    # Reverse
    # in2:  0 <-- Slower - Faster --> 1023
    in1.off()
    print("Reverse")    
    in2.duty(900)  # Fast
    sleep(1)
    in2.duty(600)    # Slow
    sleep(1)
    in2.duty(300)    # Slower
    sleep(1)
    in2.duty(0)     # Stopped
    sleep(1)
