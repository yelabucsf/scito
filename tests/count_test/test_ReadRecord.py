from unittest import TestCase
from scito_count.ReadRecord import *


class TestFQAdtAtac(TestCase):
    def setUp(self) -> None:
        read_block = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        self.FQAdtAtac = FQAdtAtac(read_block=read_block, read_start=0, read_end=16)

    def test_parse_adt_atac(self):
        print("!!!!!{}".format([self.FQAdtAtac.seq, self.FQAdtAtac.quality_score]))
        self.assertEqual(self.FQAdtAtac.seq, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:16])



