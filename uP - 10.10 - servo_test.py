'''
 10.10 - Control a 5 Volt mini servo motor.

 This sketch shows how to control a 5 Volt mini servo motor.
 
 This sketch works by converting a degree value to a PWM value. It does this
 via a map() function, that works similar to the Arduino map() function.
 
  
 Components
 ----------
  - ESP32
  - 5V mini servo motor
  -     Red    --> 5V
  -     Black  --> GND
  -     Orange --> GPIO 2
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * PWM: http://docs.micropython.org/en/latest/esp32/quickref.html#pwm-pulse-width-modulation
 * The Arduino map() function: https://www.arduino.cc/reference/en/language/functions/math/map/
 
 Original work by George Bantique, TechToTinker, https://techtotinker.blogspot.com/2020/09/006-micropython-tutorial-how-to-control.html
 
 Beware:
 A 5V mini servo will be able to get enough current from the ESP32 5V pin. If you are using a
 larger servo, consider connecting it to external power.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

# Load the machine module for GPIO and PWM
# Control servo motor with MicroPython
# Author: George Bantique, TechToTinker
# Date: September 15, 2020
# Original: https://techtotinker.blogspot.com/2020/09/006-micropython-tutorial-how-to-control.html

import machine
# Load the time module for the delays
import time

# Create a regular p2 GPIO object
servo_pin = machine.Pin(2, machine.Pin.OUT)

# Create another object named pwm by
# attaching the pwm driver to the pin
pwm = machine.PWM(servo_pin)

# Set the pulse every 20ms
pwm.freq(50)

# Set initial duty to 0
# to turn off the pulse
pwm.duty(0)

# Creates a function for mapping the 0 to 180 degrees
# to 20 to 120 pwm duty values
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Creates another function for turning 
# the servo according to input angle
def servo(pwm_pin, angle):
    pwm_pin.duty(map(angle, 0, 180, 20, 120))

# Beware, your servo may not be able to move the full extend 0 to 180 degrees.
# My test servo can safely move from 20 to 170 degrees.

# To rotate the servo motor to 20 degrees
servo(pwm, 0)
time.sleep(1)

# To rotate the servo motor to 90 degrees
servo(pwm, 90)
time.sleep(1)

# To rotate the servo motor to 170 degrees
servo(pwm, 170)
time.sleep(1)

while True:
    # To rotate the servo from 20 to 170 degrees 
    # by 10 degrees increment
    for i in range(0, 170, 10):
        print("20 to 170, step ", i)
        servo(pwm, i)
        time.sleep(0.5)
    
    # To rotate the servo from 170 to 20 degrees
    # by 10 degrees decrement
    for i in range(170, 0, -10):
        print("170 to 20, step ", i)
        servo(pwm, i)
        time.sleep(0.5)
    
    