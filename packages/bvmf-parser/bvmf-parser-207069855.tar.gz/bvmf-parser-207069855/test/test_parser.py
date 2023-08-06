import csv
import os
import unittest
import zipfile

from bvmf_parser import Parser


class TestParser(unittest.TestCase):

    def test_invalid_zip_file(self):
        with self.assertRaises(zipfile.BadZipFile):
            parser = Parser(zip_file='data/COTAHIST_M022019.ZIP')

    def test_parse_symbol(self):
        parser = Parser(txt_file='data/COTAHIST_M012019_VALE3.TXT')
        parser.parse_symbol('VALE3')
        self.assertTrue(os.path.exists('VALE3.CSV'))


if __name__ == '__main__':
    unittest.main()
