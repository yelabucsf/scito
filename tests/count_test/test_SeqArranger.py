from unittest import TestCase
from scito_count.SeqArranger import *
from scito_count.SeqSync import *

s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "GROUND")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "GROUND")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "TO SYNC")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "TO SYNC")

class TestFQSeqArrangerAdtAtac(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=s3_set2, read_settings=read_set2)
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3)
        dict_reads = {"read2": ground,
                      "read3": async_file}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
        self.sync_two_reads.two_read_sync()
        self.fq_seq_arranger_adt_atac = FQSeqArrangerAdtAtac(self.sync_two_reads)

    def test_arrange_sequences(self):
        lol = self.fq_seq_arranger_adt_atac.arrange_sequences()
        test_lol = next(lol)
        self.assertEqual(test_lol.read_id, '@A00351:376:HC5C3DSXY:3:2412:16721:32800 2:N:0:CACGAGAA')
        self.assertEqual(test_lol.seq, 'TCGTCGGCAGGGCAG')

