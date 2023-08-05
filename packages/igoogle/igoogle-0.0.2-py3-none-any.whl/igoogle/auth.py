
from igoogle import *


import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import gsheets

import logging
#from apiclient.discovery import build


class OAuth20InstalledApp:

    def __init__(self):
        self.client_secret_file = os.environ['GOOGLE_AUTH_PATH']
        self.scopes = ['https://www.googleapis.com/auth/drive.metadata.readonly']
        self.api_service_name = 'drive'
        self.api_version = 'v3'

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.get_authenticated_service()

    def process(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        print(f"\n\n service : {self.service}")
        self.list_drive_files(orderBy='modifiedByMeTime desc', pageSize=5)

    def get_authenticated_service(self):
        self.flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, self.scopes)
        #print(f"\n\n flow : {self.flow}")
        self.credentials = self.flow.run_console()
        #print(f"\n\n credentials : {self.credentials}")
        self.service = build(self.api_service_name, self.api_version, credentials=self.credentials)

class Gsheet:

    def __init__(self):
        self.client_secret_file = os.environ['GOOGLE_AUTH_PATH']
        self.sheets = gsheets.Sheets.from_files(self.client_secret_file, '~/storage.json')
