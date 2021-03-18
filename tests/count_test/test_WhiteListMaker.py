from unittest import TestCase
import os
from scito_count.ProcessSettings import *
from scito_count.WhiteListMaker import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")

s3_settings = S3SettingsWhitelist(conf, "WHITELIST")
outdir = os.path.join("../../whitelists", "test_list.whl")
class TestWhiteListMaker(TestCase):
    def setUp(self) -> None:
        self.wl_maker = WhiteListMaker(s3_settings)



    def test_export_whitelist(self):
        self.wl_maker.export_whitelist(outdir)
        self.assertEqual('GGATAGGGTCATAGCTAACAG', self.wl_maker.whitelist[0])
