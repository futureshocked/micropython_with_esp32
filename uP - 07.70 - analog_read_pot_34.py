'''
 07.70 - Read a potentiometer

 This sketch shows how to read a potentiometer and use it to control
 the brightness of an LED.

 When the button is pressed, the LED turns on for 500msec.

 Components
 ----------
  - ESP32
  - 330Ohm resistor for the LED
  - 5mm LED
  -     Connect anode to GPIO 21
  -     Connect cathode to GND via the resistor
  - 10KOhm potentiometer
  -     Connect the pin to GPIO 34
  -     Connect one of the side pins to 3.3V
  -     Connect the last pin to GND
  - Wires
  - Breadboard

 Documentation:
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 sleep_ms: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep_ms
 ADC: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#adc-analog-to-digital-conversion
 int(): https://docs.python.org/3/library/functions.html#int

 Beware:
 By default, ADC values are 12 bits, therefore they range from 0 to 4095.
 By default, PWM values are 10 bits, therefore they range from 0 to 1023.
 We must scale a ADC value to the PWM range to correctly control the LED.
 To do so, divide 1023/4095 = 0.24, and multiply the actual ADC value by 0.24.

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import ADC, Pin, PWM
from time import sleep

pwm21 = PWM(Pin(21))    # create ADC object on ADC pin
adc = ADC(Pin(34))     # create an LED object

adc.atten(ADC.ATTN_11DB)  # Full range: 3.3v

while True:
    pot_value = adc.read()
    pwm_value = int(pot_value * 0.25)
    print("pot: ", pot_value, ", pwm: ", pwm_value)
    pwm21.duty(pwm_value)  # 0.24 derives from scaling 0..4095 to 0..1023 =>
    sleep(0.1)
