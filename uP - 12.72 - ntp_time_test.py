'''
 12.72 - Real time clock with ntptime

 The ESP32 has a reat time clock (RTC) that you can use to keep the time and date.
 
 Once you set the clock, it will keep the date and time until it looses power.
 
 This sketch shows how to set the clock automatically using the ntptime library.
 
 With ntptime, your ESP32 can get the current time from a compatible ntpd server. You can find
 one near you at https://www.ntppool.org.
 
 This sketch also shows how to adjust the time and date information recieved from the ntpd server
 to your local timezone.
 
 Use this script along side the wifi_settings_test.json file which contains your wifi network
 credentials.
  
 Components
 ----------
  - ESP32 only
  - Wires
  - Breadboard

 Documentation:
 RTC: source http://docs.micropython.org/en/latest/library/machine.RTC.html#machine-rtc
 ntpd servers near you: https://www.ntppool.org/en/
 Time at your location: https://time.is/
 ntptime library: https://mpython.readthedocs.io/en/master/library/micropython/ntptime.html
 json library: https://docs.python.org/3/library/json.html
 utime library: https://docs.micropython.org/en/latest/library/utime.html
 network library: https://docs.micropython.org/en/latest/library/network.html#module-network
 usys: https://docs.micropython.org/en/latest/library/usys.html?highlight=usys
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

# UTC time: https://time.is/UTC

import network, sys
import ujson as json 
import ntptime
import utime
from machine import RTC
from time import sleep

with open("/wifi_settings_test.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

def do_connect():
    wlan.active(True)             # Activate the interface so you can use it.
    if not wlan.isconnected():    # Unless already connected, try to connect.
        print('connecting to network...')
        wlan.connect(settings["wifi_name"], settings["password"])  # Connect to the station using
                                                                   # credentials from the json file.
        if not wlan.isconnected():
            print("Can't connect to network with given credentials.")
            usys.exit(0)  # This will programmatically break the execution of this script and return to shell.
    print('network config:', wlan.ifconfig())

wlan = network.WLAN(network.STA_IF) # This will create a station interface object.
                                    # To create an access point, use AP_IF (not covered here).
do_connect()

ntptime.host = "0.au.pool.ntp.org"  # Find your local NTP server here: https://www.ntppool.org/en/

rtc = RTC()

if wlan.isconnected() == True:    # This test is redundant since connection is tested in the do_connect() method
        try:
          print("Utime time before synchronization：%s" %str(utime.localtime()))
          #make sure to have internet connection
          ntptime.settime()
          print("Utime/UTC time after synchronization：%s" %str(utime.localtime()))
        except:
          print("Error syncing time")
          usys.exit()
else:
    print("Not connected")
    sys.exit()

current_time_date_utc = utime.localtime() # The ntptime library will set utime.localtime to the UTC time automatically.
current_time_date_local = utime.mktime(current_time_date_utc)    # Create a new time object to store the local time.
current_time_date_local += 11*3600 # Sydney is 11 hours ahead of UTC. One hour has 60*60 = 3600 seconds
print("Local time:, ", utime.localtime(current_time_date_local))  # This shows time at your location

# You can set the ESP32 RTC to your local time, or UTC time. Bellow, I am setting to UTC:
'''
rtc.datetime(  (current_time_date_utc[0],
                current_time_date_utc[1],
                current_time_date_utc[2],
                0,
                current_time_date_utc[3],
                current_time_date_utc[4],
                current_time_date_utc[5],
                0))
'''
# ... and here, setting the RTC to local time:
rtc.datetime(  (utime.localtime(current_time_date_local)[0],
                utime.localtime(current_time_date_local)[1],
                utime.localtime(current_time_date_local)[2],
                0,
                utime.localtime(current_time_date_local)[3],
                utime.localtime(current_time_date_local)[4],
                utime.localtime(current_time_date_local)[5],
                0))

utc_date_time = rtc.datetime()

print()
print("UTC time: ", utc_date_time) # print date and time as set in the RTC
print("UTC date (year, month, day, day of week): ",  utc_date_time[0],
                                                      "/",
                                                      utc_date_time[1],
                                                      "/",
                                                      utc_date_time[2],
                                                      " | ",
                                                      utc_date_time[3])
print("UTC time (hour:minute:second): ",      utc_date_time[4],
                                              ":",
                                              utc_date_time[5],
                                              ":",
                                              utc_date_time[6])
print("Local time:, ", utime.localtime(current_time_date_local))
print("Local date (year, month, day, day of week): ",   utime.localtime(current_time_date_local)[0],
                                                        "/",
                                                        utime.localtime(current_time_date_local)[1],
                                                        "/",
                                                        utime.localtime(current_time_date_local)[2],
                                                        " | ",
                                                        utime.localtime(current_time_date_local)[3])
print("Local time (hour:minute:second): ",   utime.localtime(current_time_date_local)[3],
                                              ":",
                                              utime.localtime(current_time_date_local)[4],
                                              ":",
                                              utime.localtime(current_time_date_local)[5])                                


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
    sleep(1)    
