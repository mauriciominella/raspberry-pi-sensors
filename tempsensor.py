from __future__ import print_function  
import Adafruit_DHT
import time
# import many libraries
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from oauth2client.service_account import ServiceAccountCredentials 
import datetime


# ------ User Settings ------
SENSOR_LOCATION_NAME = "Office"
# MINUTES_BETWEEN_READS = 60
MY_SPREADSHEET_ID = "1aElvUgojGj9XqDijivIEmD44EwbR1q_m8v2AV6QDN9o"

def main():
    humidity, temp_c = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    print(temp_c)
    print(format(humidity, ".2f"))
    # update_sheet('temperature', temp_c, humidity)
    #time.sleep(60*MINUTES_BETWEEN_READS)

def update_sheet(sheetname, temperature, humidity):
    """update_sheet method:
        appends a row of a sheet in the spreadsheet with the
        the latest temperature, pressure and humidity sensor data
        """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'raspberry-pi-google-credentials.json', SCOPES)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API, append the next row of sensor data
    # values is the array of rows we are updating, its a single row
    values = [ [ str(datetime.datetime.now()),
                'Temperature', temperature, 'Humidity', humidity ] ]
    body = { 'values': values }
    # call the append API to perform the operation
    result = service.spreadsheets().values().append(
        spreadsheetId=MY_SPREADSHEET_ID,
        range=sheetname + '!A1:G1',
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body).execute()


if __name__ == '__main__':
    main()
