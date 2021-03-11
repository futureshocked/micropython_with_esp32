'''
 12.80 - Write/append data to a CSV file.

The ESP32 contains a flash memory file system that is accessible via micropython.

In this example, I will show you how to store dymmy sensor data to a CSV file.

You can retrieve the data by downloading the file to your computer, or
by using a seperate program (I provide this in the next lecture).
  
 Components
 ----------
  - ESP32
  - Nothing else.

 Documentation:
 * Micropython "open" function: http://docs.micropython.org/en/latest/library/builtins.html?highlight=open#open
 * Python "open" function: https://docs.python.org/3/library/functions.html#open
 * Flash partitions: http://docs.micropython.org/en/latest/library/esp32.html#flash-partitions
 * ESP flash size: https://mpython.readthedocs.io/en/master/library/micropython/esp.html#esp.flash_size
 * uos.stat: http://docs.micropython.org/en/latest/library/uos.html#uos.stat
 * CPython os.stat: https://docs.python.org/3/library/os.html#os.stat
 
 Beware:
 To the best of my knowledge, there is no function that returns the amount of flash space is available for
 your script to use. So, you need to consider tracking the space that your data file takes up programmatically.
 A way to do this is to use the uos.stat() function, which returns information about a given file. I give an
 example of how to use this function below.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''


import random
from esp32 import Partition
import esp
import uos

filename = "csv_data_file.txt"

# Get some statistics:
print("Available flash space: ", esp.flash_size()) # This will give you the total amount of Flash available

partition = Partition(Partition.RUNNING)
print(partition.info()) # Print out information about the running flash partition on which you can store your files.

file_stats = uos.stat(filename)
print("File size before write: ", file_stats[6])  # the item at index 6 of the tupple contains the total bytes in the file.

# This loop will add 10 lines that contain dummy comma-delimited data.
for x in range(10):
    random_temp = random.randint(0, 50)
    random_humi = random.randint(20, 90)
    random_pres = random.randint(900, 1100)  # in hPa
    
    file = open (filename, "a")  # Append to the end of an existing file
    #new_entry = str(random_temp) + "," + str(random_humi) + "," + str(random_pres) + "\n"  # Create the string that contains the dummy CSV data
    new_entry = "{},{},{}\n".format(random_temp,random_humi,random_pres)
    file.write(new_entry)
    file.close()

file_stats = uos.stat(filename)
print("File size after write: ", file_stats[6]) # the item at index 6 of the tupple contains the total bytes in the file.