from unittest import TestCase

from scito_count.BlockSplit import *
from scito_count.ProcessSettings import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "FULL R2 UPLOAD TEST")

class TestBlockSplit(TestCase):
    def setUp(self) -> None:
        self.block_split = BlockSplit(s3_set)

    def test__get_bgzf_block_size(self):
        lol = self.block_split._get_bgzf_block_size()
        self.assertEqual(lol, 3602)

    def test_generate_blocks(self):
        lol = self.block_split.generate_blocks()
        next(lol)
        next_lol = next(lol)
        self.assertEqual(next_lol, (3602, 7335))

    def test_generate_blocks_full(self):
        lol = list(self.block_split.generate_blocks())
        self.assertEqual(len(lol), 1000)