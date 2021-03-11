'''
 12.20 - Clock frequency control

 The ESP32 clock normally operates at 240 MHz. If your gadget is powered by battery, and you want to
 increase its life, you can choose to reduce the clock frequency (or/and to put the ESP32 to sleep, which
 I test in a seperate lecture).
 
 This script demonstrates how to control the clock frequency of the ESP32.
 
 To measure the power consumption at each of the clock rates, connect an external power supply to
 the 5V and GND pins, and set the supply to 5.0V.
 
 If your power supply can provide stable 3.3V output, you can also connect it to the 3.3V pin. Beware,
 the 3.3V pin does not include a power regulator. If your input voltage exceeds 3.3V, your ESP32 will be
 damaged.
 
 Save this script as "boot.py" so that it will be executed when the ESP32 is powered up by your bench
 power supply.
  
 Components
 ----------
  - ESP32 only.
  - Wires
  - Breadboard

 Documentation:
 Timers: http://docs.micropython.org/en/latest/esp32/quickref.html#timers
 Board control, frequency: http://docs.micropython.org/en/latest/esp32/quickref.html?highlight=osdebug#general-board-control
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import machine
from time import sleep

while True:
    machine.freq(240000000)
    print(machine.freq())
    sleep(5)

    machine.freq(80000000)
    print(machine.freq())
    sleep(5)

    machine.freq(40000000)
    print(machine.freq())
    sleep(5)



