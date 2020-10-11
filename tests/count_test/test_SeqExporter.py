from unittest import TestCase
from scito_count.SeqExport import *
from scito_count.ProcessSettings import *

s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R3")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R3")




class TestSeqExport(TestCase):
    def setUp(self) -> None:
        pass

    def test_s3_upload_r2(self):
        read2 = FQFile(s3_settings=s3_set2, read_settings=read_set2, qc_scale="phred")
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        arranged_read2 = FQAdtAtacArranger((read2, read3))
        self.seq_export_arr_r2 = SeqExport(arranged_read2)
        self.seq_export_arr_r2.s3_upload(s3_set2)
        self.assertEqual(1, 2 - 1)

    def test_s3_upload_r3(self):
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        self.seq_export_r3 = SeqExport(read3)
        self.seq_export_r3.s3_upload(s3_set3)
        self.assertEqual(1, 2 - 1)
