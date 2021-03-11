'''
 15.40b - Combine an 1.3" OLED with the SH1106 controller, a BME280 sensor and Wifi/IFTTT

 Contains supporting variables and functions needed by oled_bme_280_IFTTT_modular.py".

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import ntptime
from machine import RTC, Pin
import ujson as json
import urequests  as requests


internet_time_acquired = False
iftt_notification_counter = 0 # Use this counter to prevent too many IFTTT notifications
                               # A notification will be sent at most once every 10 minutes (600 seconds).
iftt_notification_interval_sec = 60
iftt_notification_sent = False

headers = {"Content-Type": "application/json"}

def do_connect(wlan, settings):
    wlan.active(True)             # Activate the interface so you can use it.
    if not wlan.isconnected():    # Unless already connected, try to connect.
        print('connecting to network...')
        wlan.connect(settings["wifi_name"], settings["password"])  # Connect to the station using
                                                                   # credentials from the json file.
        print("Connected to Wifi:", wlan.isconnected())
        if not wlan.isconnected():
            print("Can't connect to network with given credentials.")
            return(1)
    print('network config:', wlan.ifconfig())
    return(0)

def do_disconnect(wlan):
    wlan.active(False)
    print("Wifi disconnected.")

def draw_static_screen(display):
    display.text('Temp: ', 5, 5, 1)
    display.text('Humi: ', 5, 15, 1)
    display.text('Pres: ', 5, 25, 1)
    display.text('Time: ', 5, 35, 1)
    display.text('Date: ', 5, 45, 1)
    display.text('Starting... ', 5, 55, 1)

def clear_dynamic_screen(display):
    display.fill_rect(45, 0, 83, 64, 0)
    display.fill_rect(0, 55, 128, 10,0)

def draw_dynamic_screen(temp="N/A",humi="N/A",press="N/A",display=None):
    local_time = "N/A"
    local_date = "N/A"
    print("Internet time acquired", internet_time_acquired)
    if (internet_time_acquired == True):
        rtc = RTC()
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

        local_time = str(date_time[4]) + ":" + str(date_time[5]) + ":" + str(date_time[6])
        local_date = str(date_time[0]) + "/" + str(date_time[1]) + "/" + str(date_time[2])

    print(local_time)

    display.text(temp, 45, 5, 1)
    display.text(humi, 45, 15, 1)
    display.text(press, 45, 25, 1)
    display.text(local_time, 45, 35, 1)
    display.text(local_date, 45, 45, 1)
    print("iftt_notification_sent: ", iftt_notification_sent)
    print("iftt_notification_counter: ", iftt_notification_counter)
    display.text('IFTTT in', 5, 55, 1)
    display.text(str(iftt_notification_interval_sec-iftt_notification_counter) + "s",80,55,1) # This will show a countdown.

def get_internet_time(wlan):
    global internet_time_acquired
    ntptime.host = "0.au.pool.ntp.org"  # Find your local NTP server here: https://www.ntppool.org/en/
    print("GET TIME Connected? ", wlan.isconnected())
    rtc = RTC()

    try:
          print("Utime time before synchronization：%s" %str(utime.localtime()))
          #make sure to have internet connection
          ntptime.settime()
          print("Utime/UTC time after synchronization：%s" %str(utime.localtime()))
          current_time_date_utc = utime.localtime() # The ntptime library will set utime.localtime to the UTC time automatically.
          current_time_date_local = utime.mktime(current_time_date_utc)    # Create a new time object to store the local time.
          current_time_date_local += 11*3600 # Sydney is 11 hours ahead of UTC. One hour has 60*60 = 3600 seconds
          print("Local time:, ", utime.localtime(current_time_date_local))  # This show time at your location

          rtc.datetime(  (utime.localtime(current_time_date_local)[0],
                utime.localtime(current_time_date_local)[1],
                utime.localtime(current_time_date_local)[2],
                0,
                utime.localtime(current_time_date_local)[3],
                utime.localtime(current_time_date_local)[4],
                utime.localtime(current_time_date_local)[5],
                0))

          internet_time_acquired = True
          print("Internet time received: ", internet_time_acquired)
    except:
          print("Error syncing time")

def post_to_ifttt(temp,humi,press,wlan,settings,url):
    global iftt_notification_counter
    global iftt_notification_sent

    print("post_to_ifttt, iftt_notification_counter: ", iftt_notification_counter)
    if (iftt_notification_counter == 0):
        data = { "value1" : temp, "value2" : humi, "value3" : press }

        print("Sending POST request to IFTTT...with this content: ", data)
        do_connect(wlan,settings)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        ifttt_back = response.content

        if (internet_time_acquired == False):  # In case we were unable to get the Internet time at boot
            get_internet_time(wlan)

        print("Response from IFTTT: ", ifttt_back)
        iftt_notification_sent = True
        print("iftt_notification_sent: ", iftt_notification_sent)
        print("iftt_notification_counter: ", iftt_notification_counter)
        iftt_notification_counter = iftt_notification_counter + 1
    else:
        print("No notification sent.")
        iftt_notification_sent = False
        print("iftt_notification_sent: ", iftt_notification_sent)
        print("iftt_notification_counter: ", iftt_notification_counter)
        iftt_notification_counter = iftt_notification_counter + 1
        if (iftt_notification_counter == iftt_notification_interval_sec):
            iftt_notification_counter = 0
    do_disconnect(wlan)
