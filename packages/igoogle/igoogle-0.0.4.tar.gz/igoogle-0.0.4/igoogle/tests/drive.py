
import unittest
from igoogle.drive import *


def main():
    unittest.main()


@unittest.skip("showing class skipping")
class RecentFilesTestCase(unittest.TestCase):

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        #print(f"\n\n testfuncname : {inspect.stack()[0][3]}")
        url = 'https://docs.google.com/spreadsheets/d/1MM2_bUcb1vDt-9epfmP9CN5Oj62idoxzCHIUQn4CVck/edit#gid=0'
        #s = RecentFiles(url)
        #dbg.print_obj(s)

#@unittest.skip("showing class skipping")
class GsheetsTestCase(unittest.TestCase):

    gs = Gsheets('https://docs.google.com/spreadsheets/d/1kxlAuepdMnZndw59zjluvkkx6zY92_xuisjtII8xO1s/edit#gid=0')

    #@unittest.skip("demonstrating skipping")
    def test__get_sheetdf(self):
        df = self.gs.get_sheetdf('Sheet1')
        self.assertFalse(len(df) is 0)
