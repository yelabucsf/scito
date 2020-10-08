from unittest import TestCase
from scito_count.ReadArranger import *
from scito_count.SeqFile import *



class TestFQAdtAtacArranger(TestCase):
    def setUp(self) -> None:

        s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                             "ATAC ADT R2")
        read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                                 "ATAC ADT R2")


        s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                             "ATAC ADT R3")
        read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                                 "ATAC ADT R3")
        read2 = FQFile(s3_settings=s3_set2, read_settings=read_set2, qc_scale="phred")
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        self.test_read_arranger = FQAdtAtacArranger((read2, read3))



    def test_arrange(self):
        lol = next(self.test_read_arranger.arrange())
        print(lol.seq, lol.read_id, lol.quality_score)
        self.assertEqual(lol.seq, "TCGTCGGCAGCGTCAGACGAG")
        self.assertEqual(lol.quality_score, "FFFFFFFFFFFFFFFFFFFFF")

