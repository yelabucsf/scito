from unittest import TestCase
import os
from scito_count.ProcessSettings import *
from scito_count.WhiteListMaker import *

s3_settings = S3SettingsWhitelist("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "WHITELIST")
outdir = os.path.join("../../whitelists", "test_list.whl")
class TestWhiteListMaker(TestCase):
    def setUp(self) -> None:
        self.wl_maker = WhiteListMaker(s3_settings)



    def test_export_whitelist(self):
        self.wl_maker.export_whitelist(outdir)
        self.assertEqual('GGATAGGGTCATAGCTAACAG', self.wl_maker.whitelist[0])
