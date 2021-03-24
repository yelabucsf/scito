from unittest import TestCase
from scito_lambdas.lambda_utils import *
from io import StringIO

conf = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")

class Test_1(TestCase):
    def test_init_config_fromIO(self):
        with open("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini") as cfg:
            lol = StringIO(cfg.read())
        config_init = init_config(lol)
        section = list(config_init.values())[2]
        self.assertEqual(section['key'], 'anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')


    def test_init_config_fromFile(self):
        config_init = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
        section = config_init[list(config_init.keys())[2]]
        self.assertEqual(section['key'], 'anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')


class Test_2(TestCase):
    def test_construct_s3_interface(self):
        s3_interface = construct_s3_interface('ucsf-genomics-prod-project-data',
                                              'anton/scito/mock/fastq/config_test.ini')

        config_buf = StringIO(s3_interface.s3_obj.get()["Body"].read().decode('utf-8'))
        config_init = init_config(config_buf)
        section = list(config_init.values())[2]
        self.assertEqual(section['key'], 'anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')


class Test_3(TestCase):
    def test_config_sqs_import(self):
        config_buf = config_ini_to_buf('[local test]\nbucket = ucsf-genomics-prod-project-data\n'
                                       'key = anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')
        config_init = init_config(config_buf)
        section = list(config_init.values())[0]
        self.assertEqual(section['key'], 'anton/scito/mock/fastq/downsamp/small_R2.fastq.gz')

    def test_parse_range(self):
        parsed_range = parse_range([0, 12345])
        self.assertTrue(isinstance(parsed_range,str))
        self.assertEqual(parsed_range, '0-12345')

    def test_construct_process_name(self):
        process_name = construct_process_name(config=conf, prefix='unit-test')
        self.assertTrue(isinstance(process_name, str))
        self.assertEqual(process_name, 'unit-test_downsamp_seed100_ADT_own_S19_L003_R2_001')

    def test_extract_technology_config(self):
        technology = extract_technology_config(config=conf)
        self.assertTrue(isinstance(technology, str))
        self.assertEqual(technology, 'scito ATAC')

