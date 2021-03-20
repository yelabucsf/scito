from unittest import TestCase
from scito_count.blind_byte_range import *
from scito_lambdas.lambda_utils import init_config

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
s3_set = S3Settings(conf, "FULL R2 UPLOAD TEST")


class Test(TestCase):
    def test_blind_byte_range(self):
        blind_range = blind_byte_range(s3_set)
        next(blind_range)
        lol = next(blind_range)
        self.assertEqual(lol[0], int(1e9 - 18))
