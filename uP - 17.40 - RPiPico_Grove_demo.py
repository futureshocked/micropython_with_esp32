'''
 17.50 - Demonstration of a Raspberry Pi Pico circuit made with the Grove Shield
 
 This demo combines a Raspberry Pi Pico and these Grove components:
 
 - a Grove 16x2 I2C LCD screen
 - a DHT11 temperature and humidity sensor
 - a light sensor
 - a LED socket kit
 
 Connect a BME280 sensor and a 2x16 LCD display with the PCF8574 controller
 to pins (SDA) 14 and (SCL) 15. This is I2C bus 1 (there is also I2C bus 0).
 The LCD is a 5V device, so you should connect it to the RPi Pico VBUS pin (physical pin 40).
 The BME280 sensor is a 3.3V device so you should connect it to the RPi Pico 3V3(OUT) (physical pin 36).
 Components
 ----------
  - Raspberry Pi Pico
  - Grove shield for Raspberry Pi Pico
  - Grove cables
  - Set Grove shield voltage switch to 5V
  - DHT11 module to shield D18
  - LCD module to shield I2C1
  - Light module to shield A0
  - LED module to shield D16
  
 Documentation:
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#class-i2c-a-two-wire-serial-protocol
 * I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html#class-i2c-a-two-wire-serial-protocol
 * Raspberry Pi Pico: https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf
 * Grove shield for Raspberry Pi Pico: https://www.seeedstudio.com/Grove-Shield-for-Pi-Pico-v1-0-p-4846.html
 
 Requires:
 * LCD1602 (library, save as "LCD1602.py"): http://47.106.166.129/Embeded/pico-micropython-grove/blob/master/I2C/lcd1602.py
 * dht11 (library, save as "dht11.py"): http://47.106.166.129/Embeded/pico-micropython-grove/blob/master/Digital/dht11.py

 Also see:
 * RPi Pico uPython examples: https://github.com/raspberrypi/pico-micropython-examples

Course:
 MicroPython with the ESP32
 https://techexplorations.com
'''

from machine import Pin, I2C, Timer,ADC
from LCD1602 import LCD1602
from time import sleep
from random import *
from dht11 import *


led_onboard = Pin(25, Pin.OUT)
dht11 = DHT(18)

sda=Pin(6)
scl=Pin(7)
i2c=I2C(1,sda=sda, scl=scl, freq=400000)

print("I2C addresses found: ", i2c.scan())

lcd = LCD1602(i2c, 2, 16)

light = ADC(0)

timer=Timer()

lcd.print("Starting...")
sleep(1)
lcd.clear()

def read_sensor_isr(timer):
    led_onboard.value(1)
    pres = randint(900, 1110)
    temp,hum = dht11.readTempHumid()
    
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print("T:")
    lcd.print(str(temp))
    lcd.setCursor(7, 0)
    lcd.print("H:")
    lcd.print(str(hum))
    lcd.setCursor(0, 1)
    lcd.print("P:")
    lcd.print(str(pres))
    lcd.setCursor(7,1)
    lcd.print("L:")
    lcd.print(str(light.read_u16()))
    led_onboard.value(0)

timer.init(freq=0.5,mode=Timer.PERIODIC,callback=read_sensor_isr)
