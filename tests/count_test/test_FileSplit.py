from unittest import TestCase
from scito_count.FileSplit import *
from scito_count.BlockSplit import *

handle = "mock_data/TEST_FASTQ.fastq.gz"


class TestFQAdtAtacSplit(TestCase):
    def setUp(self) -> None:
        block_split = BlockSplit(handle)
        split = block_split.generate_blocks()
        self.fq_adt_atac_split = FQAdtAtacSplit(block_split=split, n_parts=6)

    def test_adt_atac_ranges(self):
        self.fq_adt_atac_split.adt_atac_ranges(overlap=0)
        print(len(self.fq_adt_atac_split.ranges[0] * len(self.fq_adt_atac_split.ranges)))
        print(self.fq_adt_atac_split.ranges)
        self.assertEqual(self.fq_adt_atac_split.ranges[0][0][1], 7331)
        self.assertEqual(len(self.fq_adt_atac_split.ranges), 4)
