from unittest import TestCase
from scito_lambdas.architecture_utils import *
from scito_lambdas.lambda_utils import init_config
from ufixtures.UfixVcr import UfixVcr
from scito_lambdas.lambda_settings import settings_event_source_true_split_lambda
import os
import time


curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

class Test(TestCase):
    def setUp(self) -> None:
        self.sqs_interface = SQSInterface(conf, 'unit_test')
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)token', 'Author', 'User'],
                                           targets=[
                                               'arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                               '3A\d+', '2F\d+', ':\d+:', '\"sg-.*\"', '\"subnet-.*\"',
                                               '\"vpc-.*\"'
                                           ])

    def test_prep_queues(self):
        with self.vcr.use_cassette('architecture_utils_prep_queues.yml'):
            main_queue = prep_queues(conf, 'unit_test')
            main_sqs_exists = self.sqs_interface.queue_exists(dead_letter=False)
            dead_letter_sqs_exists = self.sqs_interface.queue_exists(dead_letter=True)
            # no need to destroy a queue, it's only in fixtures and does not exist in AWS
        self.assertTrue(main_sqs_exists)
        self.assertTrue(dead_letter_sqs_exists)

# No fixtures
    def test_build_lambda(self):
        lambda_conf = 'anton/scito/scito_count/lambda_settings/true_split_settings_TEST.json'
        lambda_interface = LambdaInterface(conf, 'genomics-Unit-test')
        self.assertFalse(lambda_interface.function_exists())
        main_queue = prep_queues(conf, 'unit_test')
        func_response, event_map_response = build_lambda(config=conf,
                                                         lambda_name='genomics-Unit-test',
                                                         lambda_settings=lambda_conf,
                                                         event_source_func=settings_event_source_true_split_lambda,
                                                         sqs_queue=main_queue)
        self.assertTrue(lambda_interface.function_exists())
