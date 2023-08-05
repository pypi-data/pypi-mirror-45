
from tests import *

from igoogle.drive import *
from . import dbg

import unittest




class RecentFilesTestCase(unittest.TestCase):

    def test_init(self):
        #print(f"\n\n testfuncname : {inspect.stack()[0][3]}")
        url = 'https://docs.google.com/spreadsheets/d/1MM2_bUcb1vDt-9epfmP9CN5Oj62idoxzCHIUQn4CVck/edit#gid=0'
        #s = RecentFiles(url)
        #dbg.print_obj(s)

class WorkSheetsTestCase(unittest.TestCase):

    def test_init(self):
        print(f"\n{'='*60}\n test_funcname : {inspect.stack()[0][3]}\n")
        url = "https://docs.google.com/spreadsheets/d/1Ogk1w1RAw163B21tzBzg1bR5SdTH_PyGsxkrcnVn51U/edit#gid=997044042"
        url = "https://drive.google.com/open?id=1Ogk1w1RAw163B21tzBzg1bR5SdTH_PyGsxkrcnVn51U"
        id = "1Ogk1w1RAw163B21tzBzg1bR5SdTH_PyGsxkrcnVn51U"
        w = WorkSheets(id)
        #dbg.print_obj(w)
        self.assertTrue( isinstance(w.worksheets, object) )

    def test_get_sheet(self):
        print(f"\n{'='*60}\n test_funcname : {inspect.stack()[0][3]}\n")
        id = "1Ogk1w1RAw163B21tzBzg1bR5SdTH_PyGsxkrcnVn51U"
        w = WorkSheets(id)
        w.get_sheet('Sheet1')
        dbg.print_obj(w)
        self.assertFalse(len(w.df) is 0)


def main():
    unittest.main()
