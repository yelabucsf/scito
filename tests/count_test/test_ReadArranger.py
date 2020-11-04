from unittest import TestCase
from scito_count.ReadArranger import *
from scito_count.SeqFile import *



class TestFQArrangerAdtAtac(TestCase):
    def setUp(self) -> None:
        read_block1 = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        read_block2 = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        read_record1 = FQAdtAtac(read_block=read_block1, read_start=0, read_end=16)
        read_record2 = FQAdtAtac(read_block=read_block2, read_start=3, read_end=21)
        self.fq_arranger_adt_atac = FQArrangerAdtAtac((read_record1, read_record2))

    def test_arrange(self):
        lol = self.fq_arranger_adt_atac.arrange()
        print(lol.seq, lol.read_id, lol.quality_score)
        self.assertEqual(lol.seq, "AGGACNATNTAACNCTNTAAC")
        self.assertEqual(lol.quality_score, "D:KGAPOJGPADOSJAGPADO")

