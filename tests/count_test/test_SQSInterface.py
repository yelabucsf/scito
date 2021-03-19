from unittest import TestCase
from scito_count.SQSInterface import *
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import *
import time




class TestSQSInterface(TestCase):
    def setUp(self) -> None:
        with open("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini") as cfg:
            lol = StringIO(cfg.read())
        config = init_config(lol)
        self.sqs_interface = SQSInterface(config, 'unit-test')
        try:
            self.sqs_interface.sqs.create_queue(QueueName=self.sqs_interface.dead_letter_name,
                                                Attributes={'DelaySeconds': self.sqs_interface.sqs_settings['DelaySeconds'],
                                                            'KmsMasterKeyId': self.sqs_interface.sqs_settings['KmsMasterKeyId']})
        except:
            pass
        self.active_sqs = self.sqs_interface.sqs.get_queue_by_name(QueueName=self.sqs_interface.dead_letter_name)

    def test_queue_exists(self):
        self.assertTrue(self.sqs_interface.queue_exists(dead_letter=True))
        self.assertFalse(self.sqs_interface.queue_exists(dead_letter=False))

    def test_messages_pending(self):
        msg_body = 'Hello World'
        self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))
        self.active_sqs.send_message(MessageBody=msg_body)
        time.sleep(30)
        self.assertTrue(self.sqs_interface.messages_pending(dead_letter=True))
        msgs = []
        for message in self.active_sqs.receive_messages():
            msgs.append(message.body)
            message.delete()
        time.sleep(60)
        self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))

