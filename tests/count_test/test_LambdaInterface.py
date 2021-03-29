from unittest import TestCase
from scito_lambdas.lambda_utils import *
from scito_count.LambdaInterface import *
from ufixtures.UfixVcr import UfixVcr

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))


class TestLambdaInterface(TestCase):
    def setUp(self) -> None:
        settings = {'profile_name': 'gvaihir'}
        self.lambda_interface = LambdaInterface(conf, 'unittests', **settings)
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['arn:aws:.*'])

    def test_function_exists(self):
        with self.vcr.use_cassette('LambdaInterface_function_exists.yml'):
            try:
                existence = self.lambda_interface.function_exists()
            except:
                existence = False
        self.assertTrue(isinstance(existence, bool))
        self.assertFalse(existence)


