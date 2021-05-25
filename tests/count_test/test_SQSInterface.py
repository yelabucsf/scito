from unittest import TestCase

from scito_count.SQSInterface import SQSInterface
from scito_lambdas.lambda_utils import *
from scito_lambdas.architecture_utils import create_queues
from ufixtures.UfixVcr import UfixVcr
import time

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))


class TestSQSInterface(TestCase):
    def setUp(self) -> None:
        settings = {'profile_name': 'gvaihir'}
        self.sqs_interface = SQSInterface(conf, 'unit-test', **settings)
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['us-west-2:\d+:unit', 'com/\d+/unit', '2F\d+%2F'])
    def test_queue_exists(self):
        with self.vcr.use_cassette('SQSInterface_queue_exists.yml'):
            create_queues(self.sqs_interface)
            self.assertTrue(self.sqs_interface.queue_exists(dead_letter=True))
            self.assertFalse(self.sqs_interface.queue_exists(dead_letter=False))

    def test_messages_pending(self):
        msg_body = 'Hello World'
        with self.vcr.use_cassette('SQSInterface_messages_pending.yml'):
            create_queues(self.sqs_interface)
            self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))
            active_sqs = self.sqs_interface.sqs.get_queue_by_name(QueueName=self.sqs_interface.dead_letter_name)
            active_sqs.send_message(MessageBody=msg_body)
            self.assertTrue(self.sqs_interface.messages_pending(dead_letter=True))
            msgs = []
            for message in active_sqs.receive_messages():
                msgs.append(message.body)
                message.delete()
            self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))


