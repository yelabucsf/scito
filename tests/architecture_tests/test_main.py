from unittest import TestCase
from scito_lambdas.main import *
from ufixtures.UfixVcr import *


curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

record = {
    's3': {
        'bucket': {
            'name': 'ucsf-genomics-prod-project-data'
        },
        'object': {
            'key': 'anton/scito/mock/fastq/test_config.ini'
        }
    }
}


class Test(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                                    '3A\d+', '2F\d+'])

    def test_finalize_message(self):
        conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

        msg_constant_part = {
            'section': 'section',
            'config': json.dumps(conf),
            'byte_range': ''
        }

        msg = finalize_message(msg_constant_part, (0, 1000))
        parsed_msg = json.loads(msg)
        config_from_msg = json.loads(parsed_msg['config'])
        self.assertTrue(isinstance(msg, str))
        self.assertEqual(config_from_msg['READ 2']['technology'], 'scito ATAC')


    def test_pipeline_config_s3(self):
        with self.vcr.use_cassette('main_pipeline_config_s3.yml'):
            conf_string = pipeline_config_s3(record)
        self.assertTrue(isinstance(conf_string, str))
        self.assertEqual(conf_string[:9], '[DEFAULT]')

# TODO


    def test_main_handler(self):
        pass