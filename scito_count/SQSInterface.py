from scito_lambdas.lambda_utils import *
from scito_count.ProcessSettings import *

import boto3

class SQSInterfaceError(Exception):
    '''Errors corresponding to misuse of SQSInterface'''


'''
class to create SQS queue, read and send messages
'''
class SQSInterface(object):
    def __init__(self, config: Dict, prefix: str):
        s3_settings = S3Settings(config, list(config.keys())[0])
        if s3_settings.profile == "":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=s3_settings.profile)

        self.sqs = session.resource("sqs")
        self.queue_name = construct_process_name(config, prefix)
        self.dead_letter_name = '_'.join([self.queue_name, 'DEAD-LETTER'])

        self.sqs_settings = {'DelaySeconds': '5',
                             'KmsMasterKeyId': 'alias/managed-sns-key',
                             'maxReceiveCount': '10'}


    def queue_exists(self, dead_letter=False) -> bool:
        try:
            self._activate_queue(dead_letter)
            return True
        except:
            return False

    def messages_pending(self, dead_letter=False) -> bool:
        if not self.queue_exists(dead_letter):
            raise SQSInterfaceError(f'SQSInterface.messages_pending(): {self.dead_letter_name if dead_letter else self.queue_name} '
                                    f'does not exist')
        active_queue = self._activate_queue(dead_letter)
        attr_to_check = ['ApproximateNumberOfMessages',
                         'ApproximateNumberOfMessagesDelayed',
                         'ApproximateNumberOfMessagesNotVisible']
        return any([x for x in attr_to_check if int(active_queue.attributes[x]) != 0])


    def _activate_queue(self, dead_letter=False):
        queue_scope = self.dead_letter_name if dead_letter else self.queue_name
        active_queue = self.sqs.get_queue_by_name(QueueName=queue_scope)
        return active_queue


