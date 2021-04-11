'''
 13.30 - Example that combines an ESP32 and
 a 2x16 I2C LCD screen with a BME280 sensor using hardware I2C

 This script shows how to combine two I2C devices connected to
 a ESP32.

 Connect a BME280 sensor and a 2x16 LCD display with the PCF8574 controller
 to GPIO (SDA) 19 and (SCL) 18. This is I2C ID 0.

 The LCD is a 5V device, so you should connect it to the ESP32 5V pin.

 The BME280 sensor is a 3.3V device so you should connect it to the ESP32 3.3V pin.


 Components
 ----------
  - ESP32
  - BME/BMP280 breakout
  -   Vcc to 3.3V
  -   GND to GND
  -   SDA to GPIO 19 (HW SDA ID 0)
  -   SCL to GPIO 18 (HW SCL ID 0)
  - 2x16 LCD (such as the HD44780) with the PCF8574 backpack.
  -     GND --> GND
  -     VCC --> 5V
  -     SDA --> GPIO 19 (HW SDA ID 0)
  -     SCL --> GPIO 18 (HW SCL ID 0)
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * String formatting operator: https://python-reference.readthedocs.io/en/latest/docs/str/formatting.html
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#class-i2c-a-two-wire-serial-protocol
 * Hardware I2C on ESP32: https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus
 * BME280_float: https://github.com/robert-hh/BME280
 * Python tuple: https://docs.python.org/3/library/stdtypes.html?highlight=tuple#tuple
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html#class-i2c-a-two-wire-serial-protocol

 Requires:
 * lcd_api.py: https://github.com/dhylands/python_lcd/blob/master/lcd/lcd_api.py
 * esp8266_i2c_lcd.py: https://github.com/dhylands/python_lcd/blob/master/lcd/esp8266_i2c_lcd.py

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import I2C, Pin, Timer
import esp8266_i2c_lcd as esp8266_lcd
from time import sleep
import bme280_float as bme280

led = Pin(21, Pin.OUT)

i2c = I2C(0)    # Using hardware I2C channel 0

lcd = esp8266_lcd.I2cLcd(i2c, esp8266_lcd.DEFAULT_I2C_ADDR, 2, 16)

lcd.clear()

bme = bme280.BME280(   i2c=i2c,
                       mode=bme280.BME280_OSAMPLE_8,
                       address=bme280.BME280_I2CADDR ) # Works ok with explicity settings

lcd.move_to(0, 0)
lcd.putstr("Starting...")
sleep(1)
lcd.clear()

def read_sensor_isr(event):
    led.on()
    print(bme.values)
    print("")
    print("Temp: ", bme.values[0], ", Pressure: ", bme.values[1], ", Humidity: ", bme.values[2])
    lcd.move_to(0, 0)
    lcd.putstr("%s %s" % (bme.values[0], bme.values[2]))
    lcd.move_to(0, 1)
    lcd.putstr("%s" % (bme.values[1]))
    led.off()

blink_timer = Timer(1)
blink_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_sensor_isr)
