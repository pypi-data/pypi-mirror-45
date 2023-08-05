
import unittest
from igoogle.drive import *
import idebug as dbg


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

    #@unittest.skip("demonstrating skipping")
    def test__init(self):
        gs = Gsheets('https://docs.google.com/spreadsheets/d/1kxlAuepdMnZndw59zjluvkkx6zY92_xuisjtII8xO1s/edit#gid=0')
        dbg.obj(gs)

    @unittest.skip("demonstrating skipping")
    def test__get_sheet(self):
        id = "1Ogk1w1RAw163B21tzBzg1bR5SdTH_PyGsxkrcnVn51U"
        w = WorkSheets(id)
        w.get_sheet('Sheet1')
        dbg.print_obj(w)
        self.assertFalse(len(w.df) is 0)
