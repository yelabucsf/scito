from unittest import TestCase
from scito_count.SeqFile import *
from scito_count.ProcessSettings import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "local test")
read_set = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                        "local test")

class TestSeqFile(TestCase):
    def setUp(self) -> None:
        self.seq_file = SeqFile(s3_settings=s3_set, read_settings=read_set)
        print(s3_set.__dict__, read_set.__dict__)

    def test_import_config(self):
        self.assertEqual(self.seq_file.profile, "gvaihir")
        self.assertEqual(self.seq_file.s3_bucket, "ucsf-genomics-prod-project-data")




class TestFastqFile(TestCase):
    def setUp(self) -> None:
        self.fq_file = FastqFile(s3_settings=s3_set, read_settings=read_set, qc_scale="phred")
    print(s3_set.__dict__, read_set.__dict__)

    def test_import_config(self):
        self.assertEqual(self.fq_file.profile, "gvaihir")
        self.assertEqual(self.fq_file.s3_bucket, "ucsf-genomics-prod-project-data")

    def test_import_record_fastq(self):
        self.fq_file.import_record_fastq()
        print(self.fq_file.read_records[0])

