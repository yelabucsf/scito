from unittest import TestCase

from scito_count.BitRecord import BitRecord, AdtAtacBus
from scito_count.ReadRecord import FQAdtAtac

read_block1 = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
read1 = FQAdtAtac(read_block=read_block1, read_start=0, read_end=16)

read_block2 = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
read2 = FQAdtAtac(read_block=read_block2, read_start=0, read_end=18)

class TestBitRecord(TestCase):
    def setUp(self) -> None:
        self.test_bin_record = BitRecord()

    def test_get_seq_fragment(self):
        seq_1 = self.test_bin_record.get_seq_fragment(read1, 0,0)
        seq_2 = self.test_bin_record.get_seq_fragment(read2, 6, 10)
        self.assertEqual(seq_1, "AGGACNATNTAACNCT")
        self.assertEqual(seq_2, "ATNTAACNCT")


class TestAdtAtacBus(TestCase):
    def setUp(self) -> None:
        self.test_adt_atac_bus = AdtAtacBus()

    def test_adt_atac_bus_callable(self):
        self.test_adt_atac_bus.construct_record((read1, read2))
        self.assertEqual(self.test_adt_atac_bus.bc, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:16])
        self.assertEqual(self.test_adt_atac_bus.umi, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[10:18])
        self.assertEqual(self.test_adt_atac_bus.seq, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:5])
