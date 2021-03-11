'''
 12.50 - Deep sleep

 The ESP32 can be set to go into deep sleep.
 
 In deep sleep mode, CPUs, most of the RAM, and all the digital peripherals are powered off.
 The only parts of the chip which can still be powered on are: RTC controller,
 RTC peripherals (including ULP coprocessor), and RTC memories (slow and fast).
 
 If your script has set internal pull-ups, disabled them before going to deep sleep to reduce
 current draw even further. (see deep-sleep documentation for an example on how to do this).
 
 This script demonstrates how to set deep sleep.
 
 For testing, we'll put the board to deep sleep unless it has just woken up.
 This will allow enough time to see the effect of deep sleep in current draw.
 Always be sure to not lock your ESP32 to deep-sleep mode.
 After your ESP32 returns from deep sleep, press the RST button to reset it.
 A restart due to the RST button being presses is reset cause 1 "machine.HARD_RESET".
 
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
 ESP32 sleep modes: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html
 Deep sleep: http://docs.micropython.org/en/latest/esp32/quickref.html#deep-sleep-mode
 Machine power-related functions: DEEPSLEEP_RESET
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

# machine constants: http://docs.micropython.org/en/latest/library/machine.html?highlight=reset_cause#machine-constants

import machine, usys

print("Reset cause: ", machine.reset_cause())

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:  # If you are testing for light sleep, use machine.SOFT_RESET
    print("Woke from a deep sleep")
    usys.exit() # # This will programmatically break the execution of this script and return to shell.
else:
    # put the device to sleep for 10 seconds
    print("Going to sleep for 10 seconds...")
    machine.deepsleep(10000)
    # you can also use machine.lightsleep(1000) to place the ESP32 in light sleep (retains RAM)