from unittest import TestCase
from scito_lambdas.architecture_utils import *
from scito_lambdas.lambda_utils import init_config
from ufixtures.UfixVcr import *
import os


curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

class Test(TestCase):
    def setUp(self) -> None:
        self.sqs_interface = SQSInterface(conf, 'unit_test')
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                                    '3A\d+', '2F\d+'])

    def test_prep_queues(self):
        with self.vcr.use_cassette('architecture_utils_prep_queues.yml'):
            main_queue = prep_queues(self.sqs_interface)
            main_sqs_exists = self.sqs_interface.queue_exists(dead_letter=False)
            dead_letter_sqs_exists = self.sqs_interface.queue_exists(dead_letter=True)
            # no need to destroy a queue, it's only in fixtures and does not exist in AWS
        self.assertTrue(main_sqs_exists)
        self.assertTrue(dead_letter_sqs_exists)