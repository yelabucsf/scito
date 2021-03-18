from unittest import TestCase

from scito_count.S3BlockSplit import *
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(conf, "FULL R2 UPLOAD TEST")

class TestBlockSplit(TestCase):
    def setUp(self) -> None:
        self.block_split = S3BlockSplit(s3_set)

    def test__get_bgzf_block_size(self):
        lol = self.block_split._get_bgzf_block_size()
        self.assertEqual(lol, 3602)

    def test_generate_blocks(self):
        lol = self.block_split.generate_blocks()
        next(lol)
        next_lol = next(lol)
        self.assertEqual(next_lol, (3602, 7335))

    def test_generate_blocks_full(self):
        ### This test runs very long >30 min. Don't run!
        lol = list(self.block_split.generate_blocks())
        self.assertEqual(len(lol), 1000)