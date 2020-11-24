from unittest import TestCase
from scito_count.SeqExport import *
from scito_count.ProcessSettings import *
from scito_count.SeqArranger import *
from scito_count.SeqSync import *


s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R3")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R3")


upl_test_s3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2 UPLOAD TEST")
upl_test_read = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                             "ATAC ADT R2 UPLOAD TEST")



class TestNativeBusTools(TestCase):
    def test_run_pipe(self):
        self.fail()
