'''
 12.10 - Timers

 This sketch shows how to use the ESP32 hardware timers to control the three segments of an
 RGB LED indepentently.
 
 The ESP32 contains 4 hardware timers. In this example, I am using timers 0, 1, 2, 3. 
  
 Components
 ----------
  - ESP32
  - an RGB LED, common cathode
  - 3 x 330Ohm current limiting resistors for the three RGB LED segments
  - Wires
  - Breadboard
  
  Connect the RGB LED to the ESP32 like this:
  
  - Common cathode (longest pin) to GND.
  - Red segment via resistor to GPIO21.
  - Blue segment via resistor to GPIO22.  
  - Green segment via resistor to GPIO23.

 Documentation:
 Timers: http://docs.micropython.org/en/latest/esp32/quickref.html#timers
 Pins and GPIO: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#pins-and-gpio
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import Pin, Timer

led1 = Pin(21, Pin.OUT)    # create output pin on GPIO21, RED
led2 = Pin(22, Pin.OUT)    # create output pin on GPIO22, BLUE
led3 = Pin(23, Pin.OUT)    # create output pin on GPIO23, GREEN

def red_blink_isr(event):   
    if led1.value() == False:
        led1.on()
    else:
        led1.off() 

def blue_blink_isr(event):   
    if led2.value() == False:
        led2.on()
    else:
        led2.off()
        
def green_blink_isr(event):   
    if led3.value() == False:
        led3.on()
    else:
        led3.off()
        
blink_timer_red = Timer(0)
blink_timer_red.init(period=250, mode=Timer.PERIODIC, callback=red_blink_isr)

blink_timer_blue = Timer(1)
blink_timer_blue.init(period=350, mode=Timer.PERIODIC, callback=blue_blink_isr)

blink_timer_green = Timer(2)
blink_timer_green.init(period=450, mode=Timer.PERIODIC, callback=green_blink_isr)

