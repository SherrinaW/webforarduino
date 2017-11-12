from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'web_arduino'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.getcw()
    credential_dir = os.path.join(home_dir, '.credentials')
    print(credential_dir)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-web_arduino.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    #The input from serial port reader is in the format "(time) (temperature)"

    credentials = get_credentials()

    service = discovery.build('sheets', 'v4', credentials=credentials)

    spreadsheet_id = '1eixMKrxvQhGK4-1mSEMtiFDOR35rWasws38I1OZuFVY'

    response = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range="A2:B3000", body={}).execute()
    print(response)

    positionCounter = 2

    # set the maximum value to be the maximum number of rows of the google sheet(3000)
    while(positionCounter < 1000):
        row = input()
        if row == "":
            continue
        row = row.split(" ")
        cell1 = row[0]
        cell2 = row[1]
        range_name = 'A{}:B{}'.format(positionCounter, positionCounter)

        body = {
            'majorDimension': "ROWS",
            'values': [[cell1, cell2]]
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="USER_ENTERED", body=body).execute()

        if not result:
            print('No data found.')
        else:
            print('Writing succesful!The result is the following:')
            print(result)

        positionCounter += 1

    print("The amount of data to be displayed has reached its maximum!Please restart the program and refresh the webpage!")

if __name__ == '__main__':
    main()
