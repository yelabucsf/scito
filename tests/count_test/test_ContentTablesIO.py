from unittest import TestCase
import struct
from scito_count.ContentTablesIO import *
from scito_count.ProcessSettings import *

from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(conf, "IO TEST FQ")


class TestContentTablesIO(TestCase):
    def setUp(self) -> None:
        self.content_tables_io = ContentTablesIO(s3_set)

    def test__private_generate_content_tables(self):
        lol = self.content_tables_io._generate_content_tables()
        next_lol = next(lol)
        self.assertEqual(next_lol.obj_size(), 224)

    def test_content_table_stream(self):
        self.content_tables_io.content_table_stream()
        lol = self.content_tables_io.content_table.read(16)
        kk = struct.unpack('<QQ', lol)
        self.assertEqual(7331, kk[1])
