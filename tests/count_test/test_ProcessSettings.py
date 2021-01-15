from unittest import TestCase
from scito_count.ProcessSettings import *


class Test(TestCase):
    def test_process_settings(self):
        config_file = "/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini"
        config_section = 'ATAC ADT R2'
        ps = process_settings(config_file, config_section, 's3_settings')
        self.assertEqual(ps['bucket'], 'ucsf-genomics-prod-project-data')

        ps = process_settings(config_file, config_section, 'read_settings')
        self.assertEqual(ps['read start'], '0')
