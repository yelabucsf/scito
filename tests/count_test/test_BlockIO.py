from unittest import TestCase
from scito_count.ProcessSettings import *
from scito_count.BlockIO import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST")

class TestBlockIO(TestCase):
    def setUp(self) -> None:
        print("lol")
        self.block_io = BlockIO(s3_set, '0-100')
        self.block_io.get_object_part()

    def test_get_object_part(self):
        self.assertEqual(self.block_io.block_start, 0)
        self.assertEqual(self.block_io.block_end, 100)
        self.assertEqual(self.block_io.data_stream.read(3), b'BUS')

    def test_close(self):
        self.block_io.close()
        self.assertTrue(self.block_io.data_stream.closed)
