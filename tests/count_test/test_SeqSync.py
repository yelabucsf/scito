from unittest import TestCase
from scito_count.SeqFile import *
from scito_count.SeqSync import *
from scito_lambdas.lambda_utils import *

config = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")

s3_set2 = S3Settings(config, "GROUND")
read_set2 = ReadSettings(config, "GROUND")
s3_set3 = S3Settings(config, "TO SYNC")
read_set3 = ReadSettings(config, "TO SYNC")


class TestFQSyncTwoReads(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=s3_set2, read_settings=read_set2, byte_range='0-9945950')
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3, byte_range='0-9945950')
        dict_reads = (ground, async_file)
        self.sync_two_reads = FQSyncTwoReads(dict_reads)

    def test_two_read_NOSYNC(self):
        lol2 = next(self.sync_two_reads.seq_files[0].read_records)
        lol3 = next(self.sync_two_reads.seq_files[1].read_records)
        self.assertFalse(self.sync_two_reads.is_synced)
        self.assertNotEqual(lol2.read_id, lol3.read_id)

    def test_two_read_sync(self):
        self.sync_two_reads.two_read_sync()
        lol2 = next(self.sync_two_reads.seq_files[0].read_records)
        lol3 = next(self.sync_two_reads.seq_files[1].read_records)
        self.assertTrue(self.sync_two_reads.is_synced)
        self.assertEqual(lol2.read_id, lol3.read_id)
