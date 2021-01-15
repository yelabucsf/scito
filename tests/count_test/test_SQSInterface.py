from unittest import TestCase
from scito_count.SQSInterface import *
from scito_count.ProcessSettings import *
from scito_utils.SQSSettings import *
import time


s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")


class TestSQSInterface(TestCase):
    def setUp(self) -> None:
        self.sqs_interface = SQSInterface(s3_set2, 'unitTest')
        self.sqs_settings = SQSSettings()
        try:
            self.sqs_interface.sqs.create_queue(QueueName=self.sqs_interface.dead_letter_name,
                                                Attributes={'DelaySeconds': self.sqs_settings.delay_seconds,
                                                            'KmsMasterKeyId': self.sqs_settings.kms_master_key_id})
        except:
            pass
        self.active_sqs = self.sqs_interface.sqs.get_queue_by_name(QueueName=self.sqs_interface.dead_letter_name)

    def test_queue_exists(self):
        self.assertTrue(self.sqs_interface.queue_exists(dead_letter=True))
        self.assertFalse(self.sqs_interface.queue_exists(dead_letter=False))

    def test_messages_pending(self):
        time.sleep(10)
        msg_body = 'Hello World'
        self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))
        time.sleep(5)
        self.active_sqs.send_message(MessageBody=msg_body)
        time.sleep(5)
        self.active_sqs.reload()
        self.assertTrue(self.sqs_interface.messages_pending(dead_letter=True))
        msgs = []
        for message in self.active_sqs.receive_messages():
            msgs.append(message.body)
        time.sleep(5)
        self.active_sqs.reload()
        self.assertFalse(self.sqs_interface.messages_pending(dead_letter=True))

