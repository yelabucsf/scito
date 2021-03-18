from unittest import TestCase
from scito_count.SeqFile import *
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")

s3_set = S3Settings(conf, "local test")
read_set = ReadSettings(conf, "local test")

class TestSeqFile(TestCase):
    def setUp(self) -> None:
        self.seq_file = SeqFile(s3_settings=s3_set, read_settings=read_set, byte_range='0-1000')
        print(s3_set.__dict__, read_set.__dict__)

    def test_import_config(self):
        self.assertEqual(self.seq_file.s3_interface.obj_size(), 9945950)




class TestFQFile(TestCase):
    def setUp(self) -> None:
        self.fq_file = FQFile(s3_settings=s3_set, read_settings=read_set, byte_range='0-1000', qc_scale="phred")
    print(s3_set.__dict__, read_set.__dict__)

    def test_import_config(self):
        self.assertEqual(self.fq_file.s3_interface.obj_size(), 9945950)

    def test_import_record_fastq(self):
        self.fq_file.import_record_fastq()
        lol = next(self.fq_file.read_records)
        self.assertEqual(lol.seq, "TCGTCGGCAG")
        self.assertTrue(issubclass(type(self.fq_file), SeqFile))
        self.assertFalse(issubclass(type(self.fq_file), List))
        print("!!!!!{}".format(lol.seq))

