from unittest import TestCase
from scito_count.SeqArranger import *
from scito_count.SeqSync import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")

s3_set2 = S3Settings(conf, "GROUND")
read_set2 = ReadSettings(conf, "GROUND")
s3_set3 = S3Settings(conf, "TO SYNC")
read_set3 = ReadSettings(conf, "TO SYNC")


class TestFQSeqArrangerAdtAtac(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=s3_set2, read_settings=read_set2, byte_range='0-500')
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3, byte_range='0-500')
        self.sync_two_reads = FQSyncTwoReads((ground, async_file))
        self.sync_two_reads.two_read_sync()
        self.fq_seq_arranger_adt_atac = FQSeqArrangerAdtAtac(self.sync_two_reads)

    def test_arrange_sequences(self):
        lol = self.fq_seq_arranger_adt_atac.read_records
        test_lol = next(lol)
        self.assertEqual(test_lol.read_id, '@A00351:376:HC5C3DSXY:3:2412:16721:32800 2:N:0:CACGAGAA')
        self.assertEqual(test_lol.seq, 'TCGTCGGCAGGGCAG')
