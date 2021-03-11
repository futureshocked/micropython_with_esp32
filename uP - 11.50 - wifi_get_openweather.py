'''
 11.50 - Get the current weather of any location on earth using the OpenWeather HTTP API.

 This sketch shows how to get the current weather of any location on earth by quering OpenWeather.com.

 To use this example, you will need to create a free account on Openweather.com, and get an API key.

 Components
 ----------
  - ESP32
  - Nothing else.

 Documentation:
 * Openweather: https://openweathermap.org/
 * Openweather JSON structure: https://openweathermap.org/current#current_JSON
 * Openweather, create or get your API key: https://home.openweathermap.org/api_keys
 * Openweather, current weather API: https://openweathermap.org/current
 * network: http://docs.micropython.org/en/latest/esp32/quickref.html?highlight=urequests#networking
 * usys: http://docs.micropython.org/en/latest/library/usys.html?highlight=sys
 * urequests: https://pypi.org/project/micropython-urequests/
 * requests: https://requests.readthedocs.io/en/master/user/install/
 * ujson: http://docs.micropython.org/en/latest/library/ujson.html?highlight=ujson
 * json: https://docs.python.org/3.5/library/json.html#module-json


 Beware:
  * The credentials for your Wifi network are stored in a separate file, with the name 'wifi_settings_ifttt.json'.
  * Edit this file to contains your network's credentials, and upload it to the flash memory of your ESP32.
  * To learn the basic usage of the JSON module, look at the C-Python json module documentation (link is above).
  * Once connected to the network, we use urequests to make HTTP requests. urequests is a subset implementation
 of the popular Python package "requests". requests is easy to use (though a bit innefficient), but I think that
 this is a reasonable tradeoff. Learn more about requests by reading its documentation.
  * To get weatcher information for your location, edit the "url" variable and replace "sydney" with the name of your city. You
  can use names such as "Port Stephens, AU", "New York, NY" or "Ciudad Sabinas Hidalgo, MX".
  * It is easier to use city IDs instead of their name and country notation so that you don't have to deal with ambiguous names.
  Look at the Openweather current weather API page for more information on the "ID" vs "q" search options. You can easily find the location ID
  by searching for your location.
  For example, the ID for New York City is "5128581", as found in its current weather URL: https://openweathermap.org/city/5128581 .

 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

import network
import urequests  as requests
import ujson as json


with open("/wifi_settings_openweather.json") as credentials_json:   # This pattern allows you to open and read an existing file.
    settings = json.loads(credentials_json.read())

headers = {"Content-Type": "application/json"}

url = "https://api.openweathermap.org/data/2.5/weather?id=5128581&units=metric&appid=" + settings["open_weather_key"]   # Using location ID
#url = "https://api.openweathermap.org/data/2.5/weather?q=New York,NY,US&units=metric&appid=" + settings["open_weather_key"] # Using city, state, country

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


response = requests.get(url)
print("Raw response: ", response)
weather_back = json.loads(response.content)

print("------------")

for x in weather_back['weather']:
    print('The weather in %s is %s with %s.' % (weather_back["name"], x['main'], x['description']))


print('Wind is %.2f meter/sec at %s degrees.' % (weather_back['wind']['speed'], weather_back['wind']['deg']))
print('Pressure at sea level is %s hPa.' % weather_back['main']['pressure'])
print('Current conditions: Humidity %s%%, temp min %.2f°C, temp max %.2f°C.' % (weather_back['main']['humidity'], weather_back['main']['temp_min'], weather_back['main']['temp_max']))
print('Feels like %.2f°C.' % weather_back['main']['feels_like'])

print("------------")
