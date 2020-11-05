from unittest import TestCase
from scito_count.SeqFile import *
from scito_count.ProcessSettings import *
from scito_count.SeqSync import *

s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "GROUND")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "GROUND")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "TO SYNC")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "TO SYNC")

class TestFQSyncTwoReads(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=s3_set2, read_settings=read_set2)
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3)
        dict_reads = {"read2": ground,
                      "read3": async_file}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')


    def test_two_read_NOSYNC(self):
        lol2 = next(self.sync_two_reads.seq_files["read2"].read_records)
        lol3 = next(self.sync_two_reads.seq_files["read3"].read_records)
        self.assertFalse(self.sync_two_reads.is_synched)
        self.assertNotEqual(lol2.read_id, lol3.read_id)



    def test_two_read_sync(self):
        self.sync_two_reads.two_read_sync()
        lol2 = next(self.sync_two_reads.seq_files["read2"].read_records)
        lol3 = next(self.sync_two_reads.seq_files["read3"].read_records)
        self.assertTrue(self.sync_two_reads.is_synched)
        self.assertEqual(lol2.read_id, lol3.read_id)
