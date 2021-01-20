from unittest import TestCase
import struct
from scito_count.ContentTablesIO import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST FQ")

class TestContentTablesIO(TestCase):
    def setUp(self) -> None:
        self.content_tables_io = ContentTablesIO(s3_set)

    def test__private_generate_content_tables(self):
        lol = self.content_tables_io._private_generate_content_tables()
        next_lol = next(lol)
        self.assertEqual(next_lol.obj_size(), 224)

    def test_content_table_stream(self):
        self.content_tables_io.content_table_stream()
        lol = self.content_tables_io.content_table.read(16)
        kk = struct.unpack('<QQ', lol)
        self.assertEqual(7331, kk[1])


