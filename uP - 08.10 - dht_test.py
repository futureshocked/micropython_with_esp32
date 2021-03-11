'''
 08.10 - DHT22 environment sensor

 This sketch shows how to use the DHT11 or DHT22 sensor.
  
 Components
 ----------
  - ESP32
  - DHT22 or DHT11:
  -      Facing the grill:
  -          Pin 1 (left-most) to 3.3V,
  -          Pin 2 to GPIO4,
  -          Pin 4 to GND
  -          (Pin 3 not connected).
  - Wires
  - Breadboard

 Documentation:
 Timers: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#timers
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 DHT: http://docs.micropython.org/en/latest/esp32/quickref.html#dht-driver
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, Timer
import dht

dht22 = dht.DHT22(Pin(4))

def take_measurement_isr(event):
    dht22.measure()
    print("Temp: ", dht22.temperature(), "°C, Humidity: ", dht22.humidity(), "%")
    

dht_timer = Timer(1)
dht_timer.init(period=5000, mode=Timer.PERIODIC, callback=take_measurement_isr)
