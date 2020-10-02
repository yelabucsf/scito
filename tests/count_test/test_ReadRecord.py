from unittest import TestCase
from scito_count.ReadRecord import *


class TestFQAdtAtac(TestCase):
    def setUp(self) -> None:
        self.FQAdtAtac = FQAdtAtac()

    def test_parse_adt_atac(self):
        read_block = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        self.FQAdtAtac.parse_adt_atac(read_block=read_block, read_start=0, read_end=16)

        print("!!!!!{}".format([self.FQAdtAtac.seq, self.FQAdtAtac.quality_score]))
        self.assertEqual(self.FQAdtAtac.seq, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:16])



