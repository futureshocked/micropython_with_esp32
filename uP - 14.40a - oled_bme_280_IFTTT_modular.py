'''
 15.40a - Combine an 1.3" OLED with the SH1106 controller, a BME280 sensor and Wifi/IFTTT

 Instead of using a single file to hold all logic, variables and functions (as in lecture 15.30a), this
 example follows a modular approach.

 This file contains only the necessary variables and logic, plus the timer interrupt service routine.

 Everything else is stored in a seperate file with the name "oled_bme_280_IFTTT_modules.py".

 This script, supported by "oled_bme_280_IFTTT_modules.py" will show sensor data and status in the display.
 Periodically, it will trigger an IFTTT email notification.

 This file requires several external modules, as listed below.

 Components
 ----------
  - ESP32
  - 1.3" OLED with the SH1106 controllerm 128x64
  -     GND --> GND
  -     VCC --> 3.3V
  -     SDA --> GPIO 25
  -     SCL --> GPIO 26
  - BME/BMP280 breakout
  -   Vcc to 3.3V
  -   GND to GND
  -   SDA to GPIO 19 (HW SDA ID 0)
  -   SCL to GPIO 18 (HW SCL ID 0)
  - 330Ohm resistor for the LED
  - 5mm LED
  - Wires
  - Breadboard

 Documentation:
 * Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 * sleep: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep
 * I2C software: https://docs.micropython.org/en/latest/library/machine.I2C.html?highlight=softi2c#machine.SoftI2C
 * I2C Hardware: https://docs.micropython.org/en/latest/esp32/quickref.html#hardware-i2c-bus
 * BME280_float: https://github.com/robert-hh/BME280
 * sh1106.py: https://github.com/robert-hh/SH1106

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import I2C, Timer, Pin
import sh1106
import bme280_float as bme280
from time import sleep
import network, utime
import ujson as json
import uP_-_14_40_-_oled_bme_280_IFTTT_modules as modules

led = Pin(21, Pin.OUT)

i2c = I2C(0)

display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

bme = bme280.BME280(   i2c=i2c,
                       mode=bme280.BME280_OSAMPLE_8,
                       address=bme280.BME280_I2CADDR ) # Works ok with explicity settings

with open("/wifi_settings_ifttt.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

url = "https://maker.ifttt.com/trigger/uPython/with/key/" + settings["ifttt_key"]

wlan = network.WLAN(network.STA_IF) # This will create a station interface object.
                                    # To create an access point, use AP_IF (not covered here).


def timer_isr(event):
    led.on()
    temperature, pressure, humidity = bme.values # multiple assignment from tuple to variables
    print("")
    print("Temp: ", temperature, ", Pressure: ", pressure, ", Humidity: ", humidity)

    # Get numerical value for temperature and generate an IFTTT notification if
    # it is over the threshold
    # Temperature is returned as "26.46C" by the BME280 library.
    # Use the Python substring operator with cast to float to get the numerical version.
    temperature_float = float(temperature[0:5])
    if (temperature_float > 25):
        modules.post_to_ifttt(temperature,humidity,pressure,wlan,settings,url)

    modules.clear_dynamic_screen(display)
    modules.draw_dynamic_screen(temperature,humidity,pressure,display)
    display.show()
    led.off()


display.init_display()
display.sleep(False)
display.rotate(True)
modules.draw_static_screen(display)
display.show()
modules.do_connect(wlan,settings)
sleep(1)
modules.get_internet_time(wlan)
modules.do_disconnect(wlan)

#timer_isr(1)    # Used for testing
#modules.do_disconnect(wlan)       # Used for testing
blink_timer = Timer(1)
blink_timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_isr)
