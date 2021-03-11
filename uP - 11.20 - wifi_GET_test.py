'''
 11.20 - Read text from a URL using a GET request.

 This sketch shows how to using Wifi to connect to a URL and retrieve text using a HTTP GET request.

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

 Beware:
 The credentials for your Wifi network are stored in a separate file, with the name 'wifi_settings_test.json'.
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
import urequests
import ujson as json

with open("/wifi_settings_test.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

url = "https://techexplorations.com/upython/hello.txt"   # URL to fetch

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

if wlan.isconnected() == True:    # This test is redundant since connection is tested in the do_connect() method
        print("Connected")
        print("My IP address: ", wlan.ifconfig()[0]) # Prints the acquired IP address
        response = urequests.get(url)
        print("Fetching content from ", url, ":")
        print("---------")
        print(response.text)
        print("---------")
else:
    print("Not connected")
