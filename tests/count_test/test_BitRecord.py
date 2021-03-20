from unittest import TestCase
from scito_count.BitRecord import BitRecord, BUSRecordAdtAtac
from scito_count.ReadRecord import FQRecordAdtAtac
import struct

read_block1 = ["@identifier", "AGGACNATATAACACTAATATCTAACTAATAC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
read1 = FQRecordAdtAtac(read_block=read_block1, read_start=0, read_end=21)

read_block2 = ["@identifier", "AGGACAATATNACACTAATATCTAACTAATAC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
read2 = FQRecordAdtAtac(read_block=read_block2, read_start=0, read_end=18)


class TestBitRecord(TestCase):
    def setUp(self) -> None:
        self.test_bin_record = BitRecord()

    def test_get_seq_fragment(self):
        seq_1 = self.test_bin_record.get_seq_fragment(read1, 0, 0)
        seq_2 = self.test_bin_record.get_seq_fragment(read2, 6, 10)
        self.assertEqual(seq_1, "AGGACNATATAACACTAATAT")
        self.assertEqual(seq_2, "ATATNACACT")


class TestAdtAtacBus(TestCase):
    def setUp(self) -> None:
        self.test_adt_atac_bus = BUSRecordAdtAtac()

    def test_adt_atac_bus_callable(self):
        read_record = self.test_adt_atac_bus.construct_record((read1, read2))
        unpacked_bc = struct.unpack('<Q', read_record[:8])
        bin_bc = f'{unpacked_bc[0]:042b}'    # Length of bin string is 42 because each nt is 2 bits and 21 nt in barcode
        AGGA = '00101000'
        self.assertEqual(AGGA, str(bin_bc[:8]))
