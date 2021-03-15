'''
 08.20 - Read temperature and humidity from the BME280 using I2C

 This sketch shows how to read sensor data from the BME280 using I2C.

 The script requires an external module (see below for source URL).

 Components
 ----------
  - ESP32 using I2C: SDA GPIO 4, SCL GPIO 22
  - BME/BMP280 breakout
  -     Connect sensor VIN to ESP32 3.3V
  -     Connect sensor GND to ESP32 GND
  -     Connect sensor SCL to ESP32 GPIO 22
  -     Connect sensor SDA to ESP32 GPIO 4
  - Wires
  - Breadboard

 Documentation:
 BME280_float: https://github.com/robert-hh/BME280
 Python tuple: https://docs.python.org/3/library/stdtypes.html?highlight=tuple#tuple
 I2C: https://docs.micropython.org/en/latest/library/machine.I2C.html#class-i2c-a-two-wire-serial-protocol

 Beware:
 Don't forget to save the library file (bme280_float.py) in the root directory of your ESP32, alongside
 this test file. If you are using a BME280 module similar to mine, its default address will be 0x76. This is
 what the library expects. If not, provide its actual address in the third parameter of the constructor.

 You can search for other sensor drivers: https://awesome-micropython.com/

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''


from machine import SoftI2C, Pin, Timer
import bme280_float as bme280

i2c = SoftI2C(scl=Pin(22), sda=Pin(4), freq=400000)

bme = bme280.BME280(   i2c=i2c,
                       mode=bme280.BME280_OSAMPLE_8,
                       address=bme280.BME280_I2CADDR ) # Works ok with explicit settings
#bme = bme280.BME280(i2c=i2c)  # Also works ok, defaults.

def read_sensor_isr(event):
    print(bme.values)
    print("")
    print("Temp: ", bme.values[0], ", Pressure: ", bme.values[1], ", Humidity: ", bme.values[2])


blink_timer = Timer(1)
blink_timer.init(period=1000, mode=Timer.PERIODIC, callback=read_sensor_isr)
