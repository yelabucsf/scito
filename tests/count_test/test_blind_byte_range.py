from unittest import TestCase
from scito_count.blind_byte_range import blind_byte_range
from scito_count.ProcessSettings import S3Settings
from scito_lambdas.lambda_utils import init_config
import os
from ufixtures.UfixVcr import UfixVcr

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))
s3_set = S3Settings(conf, "FULL R2 UPLOAD TEST")


class Test(TestCase):
    def test_blind_byte_range(self):
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)token', 'Author', 'User', '(?i)kms'],
                                           targets=[
                                               'arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                               '3A\d+', '2F\d+', ':\d+:', '\"sg-.*\"', '\"subnet-.*\"',
                                               '\"vpc-.*\"'
                                           ])
        with self.vcr.use_cassette('blind_byte_range.yml'):
            blind_range = blind_byte_range(s3_set)
            next(blind_range)
            lol = next(blind_range)
        self.assertEqual(lol[0], int(1e9 - 18))
