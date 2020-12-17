import boto3
import os
import json
from scito_count.ProcessSettings import *

'''
class to create SQS queue, read and send messages
'''
class SQSInterface(object):
    def __init__(self, s3_settings):
        if s3_settings.profile == "":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=s3_settings.profile)
        self.sqs = session.resource("sqs")
        self.queue_name = os.path.basename(s3_settings.object_key).split(".")[0]

    def create_sqs(self):
        dead_letter_name = '_'.join([self.queue_name, 'DEAD-LETTER'])
        self.sqs.create_queue(QueueName=dead_letter_name,
                              Attributes={'DelaySeconds': '5'}) # dead-letter-queue
        self.dead_letter_sqs = self.sqs.get_queue_by_name(QueueName=dead_letter_name)
        self.redrive_policy = {
            'deadLetterTargetArn': self.dead_letter_sqs.get_queue_attributes().QueueArn,
            'maxReceiveCount': '10'
        }

        self.sqs.create_queue(QueueName=self.queue_name,
                              Attributes={'DelaySeconds': '5',
                                          'RedrivePolicy': json.dumps(self.redrive_policy)}) # ToDo hardcode relevant attributes


        self.active_sqs = self.sqs.get_queue_by_name(QueueName=self.queue_name)

    def send_msg(self, msg_body):
        self.active_sqs.send_message(MessageBody=msg_body)

    def kill(self):
        self.active_sqs.delete()
        self.dead_letter_sqs.delete()
