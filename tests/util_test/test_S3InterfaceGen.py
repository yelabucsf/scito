from unittest import TestCase
from scito_utils.S3InterfaceGen import *
from scito_count.ProcessSettings import *

from scito_lambdas.lambda_utils import init_config

init_config = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(init_config, "ATAC ADT R2")


class TestS3InterfaceGen(TestCase):
    def test_new_key(self):
        interface_gen = S3InterfaceGen(s3_set, "BUS", "24")
        lol = interface_gen.new_key()
        self.assertEqual("anton/scito/mock/fastq/downsamp/small_R2.BUS.24", lol.s3_obj.key)
