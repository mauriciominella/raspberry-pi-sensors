# import many libraries
from __future__ import print_function  
import Adafruit_DHT
import time
import pickle
import os.path
from googleapiclient.discovery import build  
from httplib2 import Http  
from oauth2client import file, client, tools  
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials  
import datetime

# My Spreadsheet ID ... See google documentation on how to derive this
MY_SPREADSHEET_ID = '1aElvUgojGj9XqDijivIEmD44EwbR1q_m8v2AV6QDN9o'

def update_sheet(sheetname, temperature, humidity):  
    """update_sheet method:
       appends a row of a sheet in the spreadsheet with the 
       the latest temperature and humidity sensor data
    """
    # authentication, authorization step
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

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


def main():  
    """main method:
       reads the BME280 chip to read the three sensors, then
       call update_sheets method to add that sensor data to the spreadsheet
    """
    humidity, tempC = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    tempC = 23
    humidity = 56
    print ('Temperature: %f °C' % tempC)
    print ('Humidity: %f %%rH' % humidity)
    update_sheet("temperature", tempC, humidity)


if __name__ == '__main__':  
    main()
