
import unittest
from igoogle.auth import *



"""
class AuthTestCase(unittest.TestCase):

    def test_init(self):
        print(f"\n\n testfuncname : {inspect.stack()[0][3]}")
        url = 'https://docs.google.com/spreadsheets/d/1MM2_bUcb1vDt-9epfmP9CN5Oj62idoxzCHIUQn4CVck/edit#gid=0'
        o = OAuth20InstalledApp()
        dbg.print_obj(o)
        #self.assertEqual(o.auth, '/Users/sambong/pjts/libs/igoogle-auth.json')
"""
class GsheetsAuthTestCase(unittest.TestCase):

    def test_init(self):
        print(f"\n test_funcname : {inspect.stack()[0][3]}\n")
        g = Gsheet()
        dbg.print_obj(g)
        self.assertEqual(g.client_secret_file, "/Users/sambong/pjts/libs/igoogle/igoogle-auth.json")
        self.assertTrue( isinstance(g.sheets, object) )


def main():
    unittest.main()
