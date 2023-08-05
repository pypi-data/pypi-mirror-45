
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
        gsheet = gsheets.Sheets.from_files(os.environ['GOOGLE_AUTH_PATH'], '~/storage.json')
        self.sheets = gsheet.get(url)
        print(f"\n [spreadsheets synopsis]\n title : {self.sheets.title}\n len : {len(self.sheets)}")

    def get_sheetdf(self, sheetname):
        return self.sheets.find(sheetname).to_frame()
