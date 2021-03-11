'''
 09.20 - Use the 0.96" OLED with the SSD1306 controller (software I2C)

 This sketch shows how to display text and graphics in a the SSD1306 OLED display. 
 
  
 Components
 ----------
  - ESP32
  - 0.96" OLED with the SSD1306 controller
  -     GND --> GND
  -     VCC --> 3.3V
  -     SDA --> GPIO 26
  -     SCL --> GPIO 25
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * softI2C: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#machine.SoftI2C
 
 Requires:
 * SSD1306.py: https://gist.github.com/unforgiven512/cee0fdce1a00ecac31f40ca6820c1828
 
 Beware:
 I have tested a few methods for setting up the I2C object. Only the software I2C worked, as used below.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, SoftI2C #I2C #SoftI2C 
import SSD1306
from time import sleep
 
#i2c = I2C(scl=Pin(25), sda=Pin(26), freq=400000)  # Gives deprecation warning
#i2c = I2C(1)  # Does not work
i2c = SoftI2C(scl=Pin(25), sda=Pin(26), freq=400000)  # Using software I2C WORKS
 
oled_width = 128
oled_height = 64
oled = SSD1306.SSD1306_I2C(oled_width, oled_height, i2c)
 
while True:
    oled.fill(0)
    oled.text('Welcome', 0, 0)
    oled.text('OLED Display', 0, 10)
    oled.text('line 3', 0, 20)
    oled.text('line 4', 0, 30)        
    oled.show()
    sleep(1)
    oled.fill(1)
    oled.show()
    sleep(1)
    oled.fill(0)
    oled.show()
    sleep(1)
    oled.line(0,0,110,50,1)
    oled.show()
    sleep(1)