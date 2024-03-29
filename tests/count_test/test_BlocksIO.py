from unittest import TestCase
from scito_count.ProcessSettings import *
from scito_count.BlocksIO import BlocksIO
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(conf, "IO TEST")


class TestBlockIO(TestCase):
    def setUp(self) -> None:
        self.block_io = BlocksIO(s3_set, '0-100')
        self.block_io.get_object_part()

    def test_get_object_part(self):
        self.assertEqual(self.block_io.block_start, 0)
        self.assertEqual(self.block_io.block_end, 100)
        self.assertEqual(self.block_io.data_stream.read(3), b'BUS')

    def test_close(self):
        self.block_io.close()
        self.assertTrue(self.block_io.data_stream.closed)
