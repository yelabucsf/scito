from unittest import TestCase
from scito_count.FileSplit import *
from scito_count.BlockSplit import *
from scito_count.ProcessSettings import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "MED R2 UPLOAD TEST")

class TestFQAdtAtacSplit(TestCase):
    def setUp(self) -> None:
        block_split = BlockSplit(s3_set)
        split = block_split.generate_blocks()
        self.fq_adt_atac_split = FQAdtAtacSplit(block_split=split, n_parts=10000)

    def test_adt_atac_ranges(self):
        self.fq_adt_atac_split.adt_atac_ranges(overlap=0)
        print(len(self.fq_adt_atac_split.ranges[0] * len(self.fq_adt_atac_split.ranges)))
        self.assertEqual(self.fq_adt_atac_split.ranges[0][0], (0, 3602))
