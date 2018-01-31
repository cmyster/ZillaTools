import csv
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class UpdateSheet:
    def __init__(self, sheet_id, secret_file, token_file, csv_file):
        # type: (str, str, str, str) -> None
        """
        :type sheet_id: str
        :type secret_file: str
        :type token_file: str
        :type csv_file: str
        :rtype: None
        """
        self.sheet_id = sheet_id
        self.secret_file = secret_file
        self.token_file = token_file
        self.csv_file = csv_file
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.discovery_url = ('https://sheets.googleapis.com/$discovery/'
                              'rest?version=v4')
        self.service = discovery.build('sheets', 'v4', http=self.http,
                                       discoveryServiceUrl=self.discovery_url)

    def get_credentials(self):
        # type: (None) -> Storage
        """
        Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        :rtype: Storage
        """
        scopes = 'https://www.googleapis.com/auth/spreadsheets'
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.token_file)
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            secret_path = os.path.join(credential_dir, self.secret_file)
            flow = client.flow_from_clientsecrets(secret_path, scopes)
            flow.user_agent = 'Google Sheets API'
            credentials = tools.run_flow(flow, store)
        return credentials

    def clear_range(self, clear_range):
        # type: (str) -> None
        """
        Clears all the data in given  range
        :type clear_range: str
        :rtype: None
        """
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.sheet_id,
            body={},
            range='{}'.format(clear_range)
        ).execute()

    def update_from_csv(self, update_range):
        # type: (str) -> None
        """
        Updates a sheet from a CSV file.
        :type update_range: str
        :rtype: None
        """
        # Open file, read as csv and create hyperlinks after that.
        with open(self.csv_file, 'rb') as f:
            reader = csv.reader(f)
            rows = list(reader)
            for row in rows:
                for index, value in enumerate(row):
                    if 'http' in value:
                        value = '=HYPERLINK("' + value + '","link")'
                        row[index] = value

        self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            valueInputOption='USER_ENTERED',
            body={
                'values': rows
            },
            range='{}'.format(update_range),
        ).execute()

    def __call__(self):
        # type: (None) -> None
        """
        clears and re-creates a sheet using data CSV.
        :rtype: None
        """
        print 'Updating google sheet at ' \
              'https://docs.google.com/spreadsheets/d/{}'.format(self.sheet_id)
        self.clear_range('DATA!A:Z')
        self.update_from_csv('DATA!A:Z')
