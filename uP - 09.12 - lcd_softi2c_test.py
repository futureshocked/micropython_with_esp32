'''
 09.12 - Use the 2x16 LCD screen with the PCF8574 I2C backpack (software I2C)

 This sketch shows how to display text in a 2X16 LCD display. This display uses
 the PCF8574 I2C backpack instead of the native parallel connection to save on pins.

 Components
 ----------
  - ESP32
  - 2x16 LCD (such as the HD44780) with the PCF8574 backpack.
  -     GND --> GND
  -     VCC --> 5V
  -     SDA --> GPIO 0
  -     SCL --> GPIO 4
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * String formatting operator: https://python-reference.readthedocs.io/en/latest/docs/str/formatting.html
 # softI2C: https://docs.micropython.org/en/latest/esp32/quickref.html#software-i2c-bus

 Requires:
 * lcd_api.py: https://github.com/dhylands/python_lcd/blob/master/lcd/lcd_api.py
 * esp8266_i2c_lcd.py: https://github.com/dhylands/python_lcd/blob/master/lcd/esp8266_i2c_lcd.py

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import SoftI2C, Pin
import esp8266_i2c_lcd as esp8266_lcd # import I2cLcd
from time import sleep

#DEFAULT_I2C_ADDR = 0x27

i2c = SoftI2C(scl=Pin(4), sda=Pin(0), freq=400000)  # Using software I2C

lcd = esp8266_lcd.I2cLcd(i2c, esp8266_lcd.DEFAULT_I2C_ADDR, 2, 16)

lcd.clear()

counter = 0

while True:
    lcd.move_to(0, 0)
    lcd.putstr("2x16 LCD demo")
    lcd.move_to(0, 1)

    counter = counter + 1
    lcd.putstr("Counter: %d" % (counter))
    print("Counter: %d" % (counter))
    sleep(1)
