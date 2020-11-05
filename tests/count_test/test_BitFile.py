from unittest import TestCase
from scito_count.BitFile import *
from scito_count.SeqSync import *
from scito_count.BitRecord import *


s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R3")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R3")

ground = FQFile(s3_settings=s3_set2, read_settings=read_set2)
async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3)
dict_reads = {"read2": ground,
              "read3": async_file}
sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
sync_two_reads.two_read_sync()

class TestBUSFileAdtAtac(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=s3_set2, read_settings=read_set2)
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3)
        dict_reads = {"read2": ground,
                      "read3": async_file}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
        self.sync_two_reads.two_read_sync()
        self.bus_file_adt_atac = BUSFileAdtAtac(self.sync_two_reads)


    def test_bus_file_stream_adt_atac(self):
        self.bus_file_adt_atac.bus_file_stream_adt_atac()
        bit_rec = BitRecord()
        bc = bit_rec.dna_to_twobit('TCGTCGGCAGCGTCAG')
        umi = bit_rec.dna_to_twobit('GCTTTAAG')
        seq = bit_rec.dna_to_twobit('GCGTG')
        pack = struct.pack('<QQLLLL', bc, umi, seq, 1, 0, 0)
        lol = next(self.bus_file_adt_atac.bit_records)
        self.assertEqual(lol, pack)
