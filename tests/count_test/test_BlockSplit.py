from unittest import TestCase
from scito_count.BlockSplit import *
from scito_count.ProcessSettings import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST FQ")



class TestBlockSplit(TestCase):
    def setUp(self) -> None:
        handle = BlocksIO(s3_set, '0-101000')
        handle.get_object_part()
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
        self.assertEqual(len(lol), 14)

    def test_generate_blocks_search(self):
        handle = BlocksIO(s3_set, '7001-14000')
        handle.get_object_part()
        block_split = BlockSplit(handle)
        lol = block_split.generate_blocks()
        next_lol = next(lol)
        self.assertEqual(next_lol, (7332, 14717))

    def test_generate_blocks_search(self):
        handle = BlocksIO(s3_set, '14001-21000')
        handle.get_object_part()
        block_split = BlockSplit(handle)
        lol = block_split.generate_blocks()
        next_lol = next(lol)
        self.assertEqual(next_lol, (14718, 22153))

