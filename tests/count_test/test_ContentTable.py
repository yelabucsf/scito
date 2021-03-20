from unittest import TestCase
from scito_count.ContentTable import *
from scito_count.ProcessSettings import *
from scito_count.ContentTablesIO import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(conf, "IO TEST FQ")


class TestContentTable(TestCase):
    def test_whole_class(self):
        self.content_tab_gen = ContentTablesIO(s3_set)
        self.content_tab_gen.content_table_stream()
        lol = ContentTable(self.content_tab_gen)
        self.assertEqual(lol.content_table_arr[0][1], 7331)
