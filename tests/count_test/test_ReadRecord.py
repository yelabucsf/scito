from unittest import TestCase
from scito_count.ReadRecord import *


class TestFQAdtAtac(TestCase):
    def setUp(self) -> None:
        read_block = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        self.FQAdtAtac = FQRecordAdtAtac(read_block=read_block, read_start=0, read_end=16)

    def test_parse_adt_atac(self):
        print("!!!!!{}".format([self.FQAdtAtac.seq, self.FQAdtAtac.quality_score]))
        self.assertEqual(self.FQAdtAtac.seq, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:16])

    def test_read_block_to_text(self):
        lol = self.FQAdtAtac.fq_block_to_text()
        print(lol)
        self.assertEqual(lol, "@identifier\nAGGACNATNTAACNCT\n+\nD:KGAPOJGPADOSJA\n")
