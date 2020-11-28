from unittest import TestCase
from scito_count.BlockSearch import *

handle = "mock_data/TEST_FASTQ.fastq.gz"
handle_blind_1 = 'mock_data/TEST_FASTQ_blind_split/xaa'
handle_blind_2 = 'mock_data/TEST_FASTQ_blind_split/xab'
handle_blind_3 = 'mock_data/TEST_FASTQ_blind_split/xac'

class TestBlockSearch(TestCase):

    def test_header_search_start(self):
        block_search = BlockSearch(handle)
        self.assertEqual(0, block_search.header_search())

    def test_header_search_blind_1(self):
        block_search = BlockSearch(handle_blind_1)
        self.assertEqual(0, block_search.header_search())

    def test_header_search_blind_2(self):
        block_search = BlockSearch(handle_blind_2)
        self.assertEqual(332, block_search.header_search())

    def test_header_search_blind_3(self):
        block_search = BlockSearch(handle_blind_3)
        self.assertEqual(718, block_search.header_search())
