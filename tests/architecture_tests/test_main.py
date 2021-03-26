from unittest import TestCase
from scito_lambdas.main import *

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
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
    def test_finalize_message(self):
        msg_constant_part = {
            'section': 'section',
            'config': json.dumps(conf),
            'byte_range': ''
        }
        msg = finalize_message(msg_constant_part, (0,1000))
        parsed_msg = json.loads(msg)
        config_from_msg = json.loads(parsed_msg['config'])
        self.assertTrue(isinstance(msg, str))
        self.assertEqual(config_from_msg['local test']['key'], 'anton/scito/mock/fastq/downsamp/seed100_ADT_own_S19_L003_R2_001.fastq.gz')

    def test_pipeline_config_s3(self):
        conf_string = pipeline_config_s3(record)
        self.assertTrue(isinstance(conf_string, str))
        self.assertEqual(conf_string[:9], '[DEFAULT]')


    def test_architecture_for_main(self):
        pass

