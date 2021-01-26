from unittest import TestCase
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import *

class TestProcessSettings(TestCase):
    def test_init(self):
        conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
        process_set = ProcessSettings(conf, "local test")
        relevant_attr = ['bucket', 'key', 'profile']
        process_set.bucket, process_set.object_key, process_set.profile = [process_set._section_settings[x] for x in relevant_attr]
        self.assertEqual(process_set.object_key, 'anton/scito/mock/fastq/downsamp/seed100_ADT_own_S19_L003_R2_001.fastq.gz')

