from scito_lambdas.lambda_utils import *
from scito_count.ProcessSettings import *
import boto3

def que_name_from_arn(arn: str):
    deconstructed_arn = arn.split(':')
    return deconstructed_arn[-1]

def origin_vs_expected_queue(record: Dict, this_lambda_name: str) -> Tuple:
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    origin_sqs_interface = SQSInterface(config, this_lambda_name)
    origin_queue = que_name_from_arn(record['eventSourceARN'])
    expected_queue = origin_sqs_interface.queue_name
    return origin_queue, expected_queue


def problem_in_dead_letter_queue(sqs_interface):
    '''
    Raises an error if invoked
    '''
    active_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
    msgs = []
    for message in active_queue.receive_messages():
        msgs.append(message.body)
    raise SQSInterfaceError(f'true_split_handler(): Some messages could not be delivered and ended up in a DEAD_LETTER'
                            f' SQS queue. Please troubleshoot failed messages. Total number of failed messages: '
                            f'{len(msgs)}. First failed message looks like: \n{msgs[0]}')


class SQSInterfaceError(Exception):
    '''Errors corresponding to misuse of SQSInterface'''


class SQSInterface(object):
    def __init__(self, config: Dict, prefix: str, **kwargs):
        '''
        class to create SQS queue, read and send messages
        '''
        session = boto3.Session(**kwargs)
        self.sqs = session.resource("sqs")
        self.queue_name = construct_process_name(config, prefix)
        self.dead_letter_name = '_'.join([self.queue_name, 'DEAD-LETTER'])

        self.sqs_settings = {'KmsMasterKeyId': 'alias/managed-sns-key',
                             'maxReceiveCount': '10'}

    def queue_exists(self, dead_letter=False) -> bool:
        try:
            self._activate_queue(dead_letter)
            return True
        except:
            return False

    def messages_pending(self, dead_letter=False) -> bool:
        if not self.queue_exists(dead_letter):
            raise SQSInterfaceError(
                f'SQSInterface.messages_pending(): {self.dead_letter_name if dead_letter else self.queue_name} '
                f'does not exist')
        active_queue = self._activate_queue(dead_letter)
        active_queue.reload()
        attr_to_check = ['ApproximateNumberOfMessages',
                         'ApproximateNumberOfMessagesDelayed',
                         'ApproximateNumberOfMessagesNotVisible']
        return any([x for x in attr_to_check if int(active_queue.attributes[x]) != 0])

    def destroy(self):
        switch = [True, False]
        for state in switch:
            if self.queue_exists(dead_letter=state):
                active_queue = self._activate_queue(dead_letter=state)
                active_queue.delete()
            else:
                continue

    def _activate_queue(self, dead_letter=False):
        queue_scope = self.dead_letter_name if dead_letter else self.queue_name
        active_queue = self.sqs.get_queue_by_name(QueueName=queue_scope)
        return active_queue
