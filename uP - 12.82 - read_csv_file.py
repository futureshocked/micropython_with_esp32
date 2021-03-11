'''
 12.82 - Read data from a CSV file.

The ESP32 contains a flash memory file system that is accessible via micropython.

In this example, I will show you how to read dymmy sensor data from a CSV file.
  
 Components
 ----------
  - ESP32
  - Nothing else.

 Documentation:
 * Micropython "open" function: http://docs.micropython.org/en/latest/library/builtins.html?highlight=open#open
 * Python "open" function: https://docs.python.org/3/library/functions.html#open
 * Python format specification minilanguage: https://docs.python.org/3/library/string.html#format-specification-mini-language
 
 
 Beware:
 To the best of my knowledge, there is no function that returns the amount of flash space is available for
 your script to use. So, you need to consider tracking the space that your data file takes up programmatically.
 A way to do this is to use the uos.stat() function, which returns information about a given file. I give an
 example of how to use this function below.
 
 Course:
 MicroPython with the ESP32
 https://techexplorations.com

'''

filename = "csv_data_file.txt"

i=1
with open(filename,'r') as file:
    for line in file:
        #print("Line: ", line)
        line=line.rstrip('\n')  # remove any '\n'				
        data = line.split(',')
        print("Chars: ", len(line)," Raw:",line)
        if len(line) > 1:
            csv_row = "Row: {}\nTemp: {} °C\nHumidity: {} %\nPressure: {} hPa\n".format(i,data[0],data[1],data[2])
            print(csv_row)
        i=i+1
        
file.close()