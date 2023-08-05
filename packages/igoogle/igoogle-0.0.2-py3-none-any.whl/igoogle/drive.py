
import os
from igoogle import auth
import gsheets


class RecentFiles(auth.OAuth20InstalledApp):

    def __init__(self):
        super().__init__()

    def list_drive_files(self, **kwargs):
        self.results = self.service.files().list(**kwargs).execute()
        print(f"\n\n results :\n")
        pp.pprint(self.results)

class Gsheets:

    def __init__(self, url):
        self.client_secret_file = os.environ['GOOGLE_AUTH_PATH']
        self.gsheet = gsheets.Sheets.from_files(self.client_secret_file, '~/storage.json')
        self.sheets = self.gsheet.get(url)
        print(f"\n [spreadsheets synopsis]\n title : {self.sheets.title}\n len : {len(self.sheets)}")

    def get_sheet(self, sheetname):
        return self.sheets.find(sheetname).to_frame()
