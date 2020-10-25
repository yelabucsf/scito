from unittest import TestCase
from scito_count.BlockSplit import *

handle = "mock_data/TEST_FASTQ.fastq.gz"


class TestBlockSplit(TestCase):
    def setUp(self) -> None:
        self.block_split = BlockSplit(handle)

    def test__get_bgzf_block_size(self):
        lol = self.block_split._get_bgzf_block_size()
        self.assertEqual(lol, 7332)

    def test_generate_blocks(self):
        lol = self.block_split.generate_blocks()
        next(lol)
        next_lol = next(lol)
        self.assertEqual(next_lol, (7332, 14717))

    def test_generate_blocks_full(self):
        lol = list(self.block_split.generate_blocks())
        self.assertEqual(len(lol), 16)
