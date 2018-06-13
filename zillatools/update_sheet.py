import csv
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from common_data import BASE_SHEET


class UpdateSheet:
    def __init__(self, sheet_id, secret_file, token_file, csv_file, s_range):
        # type: (str, str, str, str, str) -> None
        """
        :type sheet_id: str
        :type secret_file: str
        :type token_file: str
        :type csv_file: str
        :type s_range: str
        :rtype: None
        """
        self.sheet_id = sheet_id
        self.secret_file = secret_file
        self.token_file = token_file
        self.csv_file = csv_file
        self.s_range = s_range
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

    def clear_range(self):
        # type: (None) -> None
        """
        Clears all the data in a given range.
        :rtype: None
        """
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.sheet_id,
            body={},
            range=self.s_range
        ).execute()

    def update_from_csv(self):
        # type: (None) -> None
        """
        Updates a sheet from a CSV file.
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
            spreadsheetId='{}'.format(self.sheet_id),
            valueInputOption='USER_ENTERED',
            body={'values': rows},
            range='{}'.format(self.s_range)
        ).execute()

    def __call__(self):
        # type: (None) -> None
        """
        clears and re-creates a sheet using data CSV.
        :rtype: None
        """
        print("Updating google sheet at {}/{}".format(
            BASE_SHEET, self.sheet_id))
        self.clear_range()
        self.update_from_csv()
