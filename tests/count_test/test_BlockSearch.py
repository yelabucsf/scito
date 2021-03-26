from unittest import TestCase
from scito_count.BlockSearch import *

file_path = "fixtures/TEST_FASTQ.fastq.gz"
file_path_1 = 'fixtures/TEST_FASTQ_blind_split/xaa'
file_path_2 = 'fixtures/TEST_FASTQ_blind_split/xab'
file_path_3 = 'fixtures/TEST_FASTQ_blind_split/xac'


class TestBlockSearch(TestCase):

    def test_header_search_start(self):
        handle = open(file_path, 'rb')
        block_search = BlockSearch(handle)
        self.assertEqual(0, block_search.header_search())

    def test_header_search_blind_1(self):
        handle = open(file_path_1, 'rb')
        block_search = BlockSearch(handle)
        self.assertEqual(0, block_search.header_search())

    def test_header_search_blind_2(self):
        handle = open(file_path_2, 'rb')
        block_search = BlockSearch(handle)
        self.assertEqual(332, block_search.header_search())

    def test_header_search_blind_3(self):
        handle = open(file_path_3, 'rb')
        block_search = BlockSearch(handle)
        self.assertEqual(718, block_search.header_search())
