'''
 11.40 - Send an email with IFTTT using a POST request.

 This sketch shows how to send an email by making a HTTP POST request to ifttt.com (webhook).

 To run this example, you will need an ifttt.com account and an API key.

 Components
 ----------
  - ESP32
  - Nothing else.

 Documentation:
 * If This Then Then, create an account: https://ifttt.com/home
 * IFTTT, webhooks FAQ: https://help.ifttt.com/hc/en-us/articles/115010230347
 * network: http://docs.micropython.org/en/latest/esp32/quickref.html?highlight=urequests#networking
 * usys: http://docs.micropython.org/en/latest/library/usys.html?highlight=sys
 * urequests: https://pypi.org/project/micropython-urequests/
 * requests: https://requests.readthedocs.io/en/master/user/install/
 * ujson: http://docs.micropython.org/en/latest/library/ujson.html?highlight=ujson
 * json: https://docs.python.org/3.5/library/json.html#module-json


 Beware:
 The credentials for your Wifi network are stored in a separate file, with the name 'wifi_settings_ifttt.json'.
 Edit this file to contains your network's credentials, and upload it to the flash memory of your ESP32.

 To learn the basic usage of the JSON module, look at the C-Python json module documentation (link is above).

 Once connected to the network, we use urequests to make HTTP requests. urequests is a subset implementation
 of the popular Python package "requests". requests is easy to use (though a bit innefficient), but I think that
 this is a reasonable tradeoff. Learn more about requests by reading its documentation.

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import network, usys
import urequests  as requests
import ujson as json
import random

with open("/wifi_settings_ifttt.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

headers = {"Content-Type": "application/json"}

url = "https://maker.ifttt.com/trigger/uPython/with/key/" + settings["ifttt_key"]

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
    print("My IP address: ")
    print(wlan.ifconfig()[0])  # Prints the acquired IP address
else:
    print("Not connected")

random_temp = random.randint(0, 50)
random_humi = random.randint(20, 90)
random_pres = random.randint(20, 90)
data = { "value1" : random_temp, "value2" : random_humi, "value3" : random_pres }

print("Sending POST request to IFTTT...with this content: ", data)
response = requests.post(url, headers=headers, data=json.dumps(data))
ifttt_back = response.content
print("Response from IFTTT: ", ifttt_back)
