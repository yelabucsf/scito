from unittest import TestCase
from scito_count.BlockSplit import *

handle_in = "mock_data/TEST_FASTQ.fastq.gz"
handle_1_in = 'mock_data/TEST_FASTQ_blind_split/xab'
handle_2_in = 'mock_data/TEST_FASTQ_blind_split/xac'



class TestBlockSplit(TestCase):
    def setUp(self) -> None:
        handle = open(handle_in, 'rb')
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



    def test_generate_blocks_search(self):
        handle_1 = open(handle_1_in, 'rb')
        block_split = BlockSplit(handle_1)
        lol = block_split.generate_blocks()
        next_lol = next(lol)
        self.assertEqual(next_lol, (332, 7717))

    def test_generate_blocks_search(self):
        handle_2 = open(handle_2_in, 'rb')
        block_split = BlockSplit(handle_2)
        lol = block_split.generate_blocks()
        next_lol = next(lol)
        self.assertEqual(next_lol, (718, 8153))