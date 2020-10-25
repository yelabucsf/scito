from unittest import TestCase
from scito_count.BlockCatalog import *
from scito_count.BlockSplit import *

handle = "mock_data/TEST_FASTQ.fastq.gz"


class TestFQAdtAtacSplit(TestCase):
    def setUp(self) -> None:
        block_split = BlockSplit(handle)
        split = block_split.generate_blocks()
        self.fq_adt_atac_catalog = FQAdtAtacCatalog(block_split=split, n_parts=4)

    def test_adt_atac_ranges(self):
        self.fq_adt_atac_catalog.adt_atac_catalog(overlap=0)
        print(len(self.fq_adt_atac_catalog.ranges[0] * len(self.fq_adt_atac_catalog.ranges)))
        print(self.fq_adt_atac_catalog.ranges)
        self.assertEqual(self.fq_adt_atac_catalog.ranges[0][1], 29576)
        self.assertEqual(len(self.fq_adt_atac_catalog.ranges), 4)
