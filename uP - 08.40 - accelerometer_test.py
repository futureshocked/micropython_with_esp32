'''
 08.40 - Read the ADXL335 analog accelerometer

 This sketch shows how to use the ADXL335 analog accelerometer.

 When the button is pressed, the LED turns on for 500msec.

 Components
 ----------
  - ESP32
  - ADXL335 accellerometer breakout
  -   x   : GPIO 32
  -   y   : GPIO 34
  -   z   : GPIO 35
  -   GND : GND
  -   VCC : 3.3V
  - Wires
  - Breadboard

 Documentation:
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 sleep_ms: http://docs.micropython.org/en/latest/library/utime.html?highlight=utime%20sleep#utime.sleep_ms
 ADC: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#adc-analog-to-digital-conversion

 Beware:
 Using the standard implementation of MicroPython on the ESP32, only the ADC1 GPIOS can be used for ADC. These are
 GPIOS 36, 39, 34, 35, 32, 33.
 We must scale a ADC value to the PWM range to correctly control the LED.
 To do so, divide 1023/4095 = 0.24, and multiply the actual ADC value by 0.24.

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import ADC, Pin, Timer

z = ADC(Pin(34))
x = ADC(Pin(32))
y = ADC(Pin(35))


x.atten(ADC.ATTN_11DB)
y.atten(ADC.ATTN_11DB)
z.atten(ADC.ATTN_11DB)

def adxl335_sensor_isr(event):
    x_value = x.read()
    y_value = y.read()
    z_value = z.read()

    print("x:", x_value, ",y: ", y_value, ",z: ", z_value)


blink_timer = Timer(1)
blink_timer.init(period=50, mode=Timer.PERIODIC, callback=adxl335_sensor_isr)
