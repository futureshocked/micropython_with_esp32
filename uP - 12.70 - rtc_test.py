'''
 12.70 - Real time clock

 The ESP32 has a reat time clock (RTC) that you can use to keep the time and date.
 
 Once you set the clock, it will keep the date and time until it looses power.
 
 This sketch shows how to set the clock, and then how to print the current date and time.
 
 The RTC retains power when the ESP32 is in deep sleep, so the clock keeps "ticking".
 
  
 Components
 ----------
  - ESP32 only
  - Wires
  - Breadboard

 Documentation:
 RTC: http://docs.micropython.org/en/latest/esp8266/quickref.html#real-time-clock-rtc
 RTC and deep sleep: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/sleep_modes.html
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

from machine import RTC
from time import sleep_ms

rtc = RTC()
# Datetime is a tuple of the form:
# (year, month, day, weekday, hours, minutes, seconds, subseconds)
# weekday and subseconds can be left 0

# Example: 17th of February 2021, 9:01
rtc.datetime((2021, 2, 17, 0, 9, 06, 00, 0)) # set a specific date and time

while True:
    date_time = rtc.datetime()
    print(date_time) # print date and time
    print("Current date (year, month, day, day of week): ",  date_time[0],
                                                              "/",
                                                              date_time[1],
                                                              "/",
                                                              date_time[2],
                                                              " | ",
                                                              date_time[3])
    print("Current time (hour:minute:second): ",   date_time[4],
                                                  ":",
                                                  date_time[5],
                                                  ":",
                                                  date_time[6])                                
    sleep_ms(1000)
    
