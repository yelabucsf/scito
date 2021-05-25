from unittest import TestCase
from scito_lambdas.lambda_utils import *
from scito_count.LambdaInterface import *
from ufixtures.UfixVcr import UfixVcr
import time

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))


class TestLambdaInterface(TestCase):
    def setUp(self) -> None:
        settings = {'profile_name': 'gvaihir'}
        self.lambda_interface = LambdaInterface(conf, 'unittests', **settings)
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)token', 'Author', 'User'],
                                           targets=[
                                               'arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                               '3A\d+', '2F\d+', ':\d+:', '\"sg-.*\"', '\"subnet-.*\"',
                                               '\"vpc-.*\"'
                                           ])

    def test_function_exists(self):
        with self.vcr.use_cassette('LambdaInterface_function_exists.yml'):
            try:
                existence = self.lambda_interface.function_exists()
            except:
                existence = False
        self.assertTrue(isinstance(existence, bool))
        self.assertFalse(existence)


    def test_destroy(self):
        settings = {'profile_name': 'gvaihir'}
        self.lambda_interface = LambdaInterface(conf, 'genomics-Unit-test', **settings)
        with self.vcr.use_cassette('LambdaInterface_destroy.yml'):
            self.assertTrue(self.lambda_interface.function_exists())
            self.lambda_interface.destroy()
            #time.sleep(15)
            self.assertFalse(self.lambda_interface.function_exists())


