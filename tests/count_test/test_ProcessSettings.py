from unittest import TestCase
from scito_count.ProcessSettings import *

class TestProcessSettings(TestCase):
    def test_init(self):
        process_set = ProcessSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                                 "local test")
        relevant_attr = ['bucket', 'key', 'profile']
        process_set.bucket, process_set.object_key, process_set.profile = [process_set._section_settings[x] for x in relevant_attr]
        self.assertEqual(process_set.object_key, 'anton/scito/mock/fastq/downsamp/seed100_ADT_own_S19_L003_R2_001.fastq.gz')

