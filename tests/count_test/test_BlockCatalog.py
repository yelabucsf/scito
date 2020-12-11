from unittest import TestCase
from scito_count.BlockCatalog import *
from scito_count.BlockSplit import *
from scito_count.ProcessSettings import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST FQ")

class TestFQAdtAtacSplit(TestCase):
    def setUp(self) -> None:
        self.block_io = BlocksIO(s3_set, '0-101000')
        self.block_io.get_object_part()
        handle = self.block_io
        block_split = BlockSplit(handle)
        block_split.generate_blocks()
        self.fq_adt_atac_catalog = FQAdtAtacCatalog(block_split=block_split, n_parts=4)

    def test_adt_atac_ranges(self):
        self.fq_adt_atac_catalog.adt_atac_catalog(overlap=0)
        list_lol = list(self.fq_adt_atac_catalog.ranges)
        self.assertEqual(list_lol[0][1], 29576)
        self.assertEqual(len(list_lol), 4)
