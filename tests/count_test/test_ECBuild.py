import os
from scito_lambdas.lambda_utils import init_config
from unittest import TestCase
from ufixtures.UfixVcr import UfixVcr
from scito_count.ECBuild import *

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

class TestECBuild(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['arn:aws:sqs:us-west-2:\d+'])
        self.ec_build = ECBuild(config=conf)

    def test_build_ec_map(self):
        ec_map = self.ec_build._construct_ec()
        line_of_ec_map = next(ec_map)
        data = ec_map.read()
        self.assertTrue(isinstance(data, bytes))
        self.assertEqual(data, b'sdlkjsadflkjasd')


