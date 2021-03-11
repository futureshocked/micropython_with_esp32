'''
 09.30 - Use the 1.3" OLED with the SH1106 controller (software or hardware I2C)

 This sketch shows how to display text and graphics in a the SH1106 OLED display. 
  
 Components
 ----------
  - ESP32
  - 1.3" OLED with the SH1106 controller
  -     GND --> GND
  -     VCC --> 3.3V
  -     SDA --> GPIO 25
  -     SCL --> GPIO 26
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * I2C software: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#machine.SoftI2C
 * I2C Hardware: https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus
 
 Requires:
 * sh1106.py: https://github.com/robert-hh/SH1106
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import I2C, Pin
import sh1106  # Source: https://github.com/robert-hh/SH1106
                      # For fonts: https://github.com/peterhinch/micropython-font-to-py
from time import sleep_ms

#i2c = SoftI2C(scl=Pin(25), sda=Pin(26), freq=400000)   # Software I2C works
#i2c = I2C(1,scl=Pin(22),sda=Pin(21),freq=400000)  # Hardware I2C also works
i2c = I2C(1)  # Hardware I2C also works

display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
display.init_display()
display.sleep(False)

display.fill(0)
display.text('Testing 1', 20, 25, 1)
display.show()
sleep_ms(1000)

display.fill(1)
display.text('Testing 2', 20, 25, 0)
display.show()
sleep_ms(1000)

display.rotate(True)
display.show()
sleep_ms(1000)

display.fill(0)
display.fill_rect(61,30,5,5,1)
display.show()
sleep_ms(1000)

for x in range(127):
    display.fill_rect(x,0,5,63,1)
    display.show()
    sleep_ms(10)
    
display.fill(0)

while True:
    for x in range(0, 127, 5):
        display.fill(0)
        display.fill_rect(x,30,5,5,1)
        display.show()


    for x in range(122, 0, -5):
        display.fill(0)
        display.fill_rect(x,30,5,5,1)
        display.show()
        
        