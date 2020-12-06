# import many libraries
from __future__ import print_function
import Adafruit_DHT
import time
import pickle
import os.path
import datetime
import csv
from pathlib import Path

def write_to_file(temperature, humidity):
    file_path = './data/sensor.csv';
    sensor_file = Path(file_path)
    date = datetime.datetime.now().isoformat()

    row_to_write = [str(date), round(temperature, 2), round(humidity, 2)]
    header = ["date", "temp", "humidity"]

    if sensor_file.is_file():
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row_to_write)
    else:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(row_to_write)


def main():
    """main method:
       reads the BME280 chip to read the three sensors, then
       call update_sheets method to add that sensor data to the spreadsheet
    """
    humidity, tempC = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    # tempC = 23
    # humidity = 56
    write_to_file(tempC, humidity)
    # print('Temperature: %f °C' % tempC)
    # print('Humidity: %f %%rH' % humidity)
# update_sheet("temperature", tempC, humidity)


if __name__ == '__main__':
    main()
