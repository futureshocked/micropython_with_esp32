'''
 15.50 - Example that combines a Raspberry Pi Pico and
 a 2x16 I2C LCD screen with a BME280 sensor using hardware I2C

 This script shows how to combine two I2C devices connected to
 a Raspberry Pi Pico.

 Connect a BME280 sensor and a 2x16 LCD display with the PCF8574 controller
 to pins (SDA) 14 and (SCL) 15. This is I2C bus 1 (there is also I2C bus 0).

 The LCD is a 5V device, so you should connect it to the RPi Pico VBUS pin (physical pin 40).

 The BME280 sensor is a 3.3V device so you should connect it to the RPi Pico 3V3(OUT) (physical pin 36).


 Components
 ----------
  - Raspberry Pi Pico
  - BME/BMP280 breakout
  -   Vcc to 3.3V
  -   GND to GND
  -   SDA to Pin 14 (I2C bus 1)
  -   SCL to Pin 15 (I2C bus 1)
  - 2x16 LCD (such as the HD44780) with the PCF8574 backpack.
  -     GND --> GND
  -     VCC --> 5V
  -     SDA --> Pin 14 (I2C bus 1)
  -     SCL --> Pin 15 (I2C bus 1)
  - Wires
  - Breadboard

 Documentation:
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#class-i2c-a-two-wire-serial-protocol
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html#class-i2c-a-two-wire-serial-protocol
 * Raspberry Pi Pico: https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf

 Requires:
 * machine_i2c_lcd: https://github.com/dhylands/python_lcd
 * BME280 from: https://gist.github.com/futureshocked/287606dd7556a82c90f86473a6cf2ed0

 Also see:
 * RPi Pico uPython examples: https://github.com/raspberrypi/pico-micropython-examples

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, I2C, Timer
from machine_i2c_lcd import I2cLcd
from time import sleep
import BME280

led_onboard = machine.Pin(25, machine.Pin.OUT)

DEFAULT_I2C_ADDR = 0x27

sda=Pin(14)
scl=Pin(15)
i2c=I2C(1,sda=sda, scl=scl, freq=400000)

print("I2C addresses found: ", i2c.scan())

lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

bme = BME280.BME280(i2c=i2c)

timer=Timer()

lcd.putstr("Starting...")
sleep(1)
lcd.clear()

def read_sensor_isr(timer):
    led_onboard.value(1)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    lcd.clear()
    lcd.putstr("%s %s\n%s" % (temp,hum,pres))
    led_onboard.value(0)

timer.init(freq=1,mode=Timer.PERIODIC,callback=read_sensor_isr)
