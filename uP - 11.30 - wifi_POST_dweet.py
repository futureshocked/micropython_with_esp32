'''
 11.30 - Send data to a dweet.io URL using a POST request.

 This sketch shows how to send data to a URL using a POST HTTP request.

 To keep this example simple, we'll use the free dweet.io web API.

 You can find the dweet 'playground' here: https://dweet.io/play/

 To run this example, you may use the example URL, as included in the script. Alternatively, you can create
 your own text file and upload it to any web server that is publicly available.

 Components
 ----------
  - ESP32
  - Nothing else.

 Documentation:
 * network: http://docs.micropython.org/en/latest/esp32/quickref.html?highlight=urequests#networking
 * usys: http://docs.micropython.org/en/latest/library/usys.html?highlight=sys
 * urequests: https://pypi.org/project/micropython-urequests/
 * requests: https://requests.readthedocs.io/en/master/user/install/
 * ujson: http://docs.micropython.org/en/latest/library/ujson.html?highlight=ujson
 * json: https://docs.python.org/3.5/library/json.html#module-json
 * Dweet.io playground: https://dweet.io/play/
 * Timers: https://micropython-docs-esp32.readthedocs.io/en/esp32_doc/esp32/quickref.html#timers

 Beware:
 The credentials for your Wifi network are stored in a separate file, with the name 'wifi_settings_dweet_test.json'.
 Edit this file to contains your network's credentials, and upload it to the flash memory of your ESP32.

 You can use this file to store your wifi network credentials as well as your prefered dweet "thing".

 If you want to create a private dweet thing, you can add a lock, using the same credentials file.

 To learn the basic usage of the JSON module, look at the C-Python json module documentation (link is above).

 Once connected to the network, we use urequests to make HTTP requests. urequests is a subset implementation
 of the popular Python package "requests". requests is easy to use (though a bit innefficient), but I think that
 this is a reasonable tradeoff. Learn more about requests by reading its documentation.

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

# This example show how to do a post request to dweet.io
from machine import Pin, Timer
import network, usys
import urequests  as requests
import ujson as json
import random


with open("/wifi_settings_dweet.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

headers = {"Content-Type": "application/json"}

url = "https://dweet.io:443/dweet/for/" + settings["thing"]

def do_connect():
    wlan.active(True)                 # Activate the interface so you can use it.
    if not wlan.isconnected():        # Unless already connected, try to connect.
        print('connecting to network...')
        wlan.connect(settings["wifi_name"], settings["password"])  # Connect to the station using
                                                                   # credentials from the json file.
        if not wlan.isconnected():
            print("Can't connect to network with given credentials.")
            usys.exit(0)  # This will programmatically break the execution of this script and return to shell.
        print('network config:', wlan.ifconfig())

wlan = network.WLAN(network.STA_IF)     # This will create a station interface object.
                                        # To create an access point, use AP_IF (not covered here).
do_connect()

if wlan.isconnected() == True:
        print("Connected")
        print("My IP address: ", wlan.ifconfig()[0])  # Prints the acquired IP address
else:
    print("Not connected")

def post_to_dweet_isr(event):
    random_temp = random.randint(0, 50)
    random_humi = random.randint(20, 90)
    data = { "temp": random_temp, "hum": random_humi }

    response = requests.post(url, headers=headers, data=json.dumps(data)) # Make a POST request
    dweet_back = json.loads(response.content)            # The response from Dweet.io comes as a JSON object.
    print("\nResponse from Dweet.io: ", dweet_back)
    print("Created: ", dweet_back["with"]["created"])
    print("Transaction: ", dweet_back["with"]["transaction"])
    print("thing: ", dweet_back["with"]["thing"])
    print("Temperature: ", dweet_back["with"]["content"]["temp"])
    print("Humidity: ", dweet_back["with"]["content"]["hum"])


dht_timer = Timer(1)
dht_timer.init(period=5000, mode=Timer.PERIODIC, callback=post_to_dweet_isr)
