'''
 14.30 - Combine an 1.3" OLED with the SH1106 controller, a BME280 sensor and Wifi/IFTTT

 This is an example script where a single file contains all logic, variables and functions.
 
 This script combines multiple modules to allow for a sensor, a display, and Wifi to operate
 together. The script will show sensor data and status in the display. Periodically, it will
 trigger an IFTTT email notification.
 
 This file requires several modules, as listed below.
  
 Components
 ----------
  - ESP32
  - 1.3" OLED with the SH1106 controllerm 128x64
  -     GND --> GND
  -     VCC --> 3.3V
  -     SDA --> GPIO 19
  -     SCL --> GPIO 18
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

from machine import I2C, Pin, Timer
import sh1106  
import bme280_float as bme280
from time import sleep
import network, sys
import ujson as json 
import ntptime
import utime
from machine import RTC
import urequests  as requests


internet_time_acquired = False
iftt_notification_counter = 0  # Use this counter to prevent too many IFTTT notifications
                               # A notification will be sent at most once every 10 minutes (600 seconds).
iftt_notification_interval_sec = 60                               
iftt_notification_sent = False

led = Pin(21, Pin.OUT)

i2c = I2C(0)  

display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

bme = bme280.BME280(   i2c=i2c,
                       mode=bme280.BME280_OSAMPLE_8,
                       address=bme280.BME280_I2CADDR ) # Works ok with explicity settings
    
with open("/wifi_settings_ifttt.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

headers = {"Content-Type": "application/json"}

url = "https://maker.ifttt.com/trigger/uPython/with/key/" + settings["ifttt_key"]

wlan = network.WLAN(network.STA_IF) # This will create a station interface object.
                                    # To create an access point, use AP_IF (not covered here).

def do_connect():
    if not wlan.isconnected():    # Unless already connected, try to connect.
        print('connecting to network ', settings["wifi_name"])
        wlan.active(True)
        sleep(0.5)
        wlan.connect(settings["wifi_name"], settings["password"])  # Connect to the station using
                                                                   # credentials from the json file.
        sleep(0.5)
        print("Connected to Wifi:", wlan.isconnected())
        if not wlan.isconnected():
            print("Can't connect to network with given credentials.")
            return(1)
    print('network config:', wlan.ifconfig())
    return(0)

def do_disconnect():
    wlan.active(False)
    print("Wifi disconnected.")
    
def draw_static_screen():
    display.text('Temp: ', 5, 5, 1)
    display.text('Humi: ', 5, 15, 1)
    display.text('Pres: ', 5, 25, 1)
    display.text('Time: ', 5, 35, 1)
    display.text('Date: ', 5, 45, 1)
    display.text('Starting... ', 5, 55, 1)

def clear_dynamic_screen():
    display.fill_rect(45, 0, 83, 64, 0)
    display.fill_rect(0, 55, 128, 10,0)
    
def draw_dynamic_screen(temp="N/A",humi="N/A",press="N/A"):
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
    
def get_internet_time():
    global internet_time_acquired
    #ntptime.host = "0.au.pool.ntp.org"  # Find your local NTP server here: https://www.ntppool.org/en/
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

def post_to_ifttt(temp="N/A",humi="N/A",press="N/A"):
    global iftt_notification_counter
    global iftt_notification_sent
    
    print("post_to_ifttt, iftt_notification_counter: ", iftt_notification_counter)
    if (iftt_notification_counter == 0):
        data = { "value1" : temp, "value2" : humi, "value3" : press } 

        print("Sending POST request to IFTTT...with this content: ", data)
        do_connect()
        response = requests.post(url, headers=headers, data=json.dumps(data))
        ifttt_back = response.content
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
    do_disconnect()
        
def timer_isr(event):
    led.on()
    if not wlan.isconnected():
        do_connect()
    
    #print(bme.values)
    temperature, pressure, humidity = bme.values # multiple assignment from tuple to variables
    print("")
    print("Temp: ", temperature, ", Pressure: ", pressure, ", Humidity: ", humidity)
    
    # Get numerical value for temperature and generate an IFTTT notification if
    # it is over the threshold
    # Temperature is returned as "26.46C" by the BME280 library.
    # Use the Python substring operator with cast to float to get the numerical version.
    temperature_float = float(temperature[0:5])
    if (temperature_float > 25):
        post_to_ifttt(temp=temperature,humi=humidity,press=pressure)
    
    clear_dynamic_screen()
    draw_dynamic_screen(temp=temperature,humi=humidity,press=pressure)
    display.show()
    led.off()
    
# Execution starts here

display.init_display()
display.sleep(False)
display.rotate(True)

draw_static_screen()

display.show()

do_connect()

get_internet_time()
 
do_disconnect()

timer_isr(1)    # Used for testing
do_disconnect()       # Used for testing
#blink_timer = Timer(1)
#blink_timer.init(period=1000, mode=Timer.PERIODIC, callback=timer_isr)
