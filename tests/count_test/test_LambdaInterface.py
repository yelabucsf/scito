from unittest import TestCase
from scito_lambdas.lambda_utils import *
from scito_count.LambdaInterface import *
import vcr

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))


class TestLambdaInterface(TestCase):
    def setUp(self) -> None:
        settings = {'profile_name': 'gvaihir'}
        self.lambda_interface = LambdaInterface(conf, 'unittests', **settings)
        self.my_vcr = vcr.VCR(
            serializer='yaml',
            cassette_library_dir=os.path.join(curr_dir, 'fixtures/cassettes'),
            record_mode='once',
            filter_headers=['X-Amz-Security-Token','X-Amz-Date','Authorization','User-Agent']
        )

    def test_function_exists(self):
        with self.my_vcr.use_cassette('LambdaInterface_function_exists.yml'):
            existence = self.lambda_interface.function_exists()
        self.assertTrue(isinstance(existence, bool))
        self.assertFalse(existence)

    def test_invoke_lambda(self):
        invocation = self.lambda_interface.invoke_lambda('unittests',
                                                         json.dumps({'payload': 123}),
                                                         InvocationType='DryRun')
        self.assertTrue(isinstance(invocation, dict))