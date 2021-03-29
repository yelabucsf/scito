from unittest import TestCase
from scito_lambdas.main import *
import vcr

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

record = {
    's3': {
        'bucket': {
            'name': 'ucsf-genomics-prod-project-data'
        },
        'object': {
            'key': 'anton/scito/mock/fastq/config_test.ini'
        }
    }
}


class Test(TestCase):
    def setUp(self) -> None:
        self.my_vcr = vcr.VCR(
            serializer='yaml',
            cassette_library_dir=os.path.join(curr_dir, 'fixtures/cassettes'),
            record_mode='once',
            filter_headers=['X-Amz-Security-Token', 'x-amz-id-2', 'Authorization', 'User-Agent']
        )

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
        with self.my_vcr.use_cassette('main_pipeline_config_s3.yml'):
            conf_string = pipeline_config_s3(record)
        self.assertTrue(isinstance(conf_string, str))
        self.assertEqual(conf_string[:9], '[DEFAULT]')

    def test_architecture_for_main(self):
        pass
