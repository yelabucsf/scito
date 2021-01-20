from unittest import TestCase
from scito_lambdas.lambda_utils import *


class Test_1(TestCase):
    def test_init_config(self):
        config_init = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
        config_sections = config_init.sections()
        section = config_init[config_sections[2]]
        self.assertEqual(section['key'], 'anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')

