from urllib.parse import unquote_plus

from scito_count.S3Interface import *
from scito_count.ProcessSettings import *


def initial_blind_split_handler(event, context):

    # download config
    record = event['Records']
    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    local_key = s3_key.replace('/', '_')
    s3_interface = S3Interface(s3_bucket, s3_key)
    if s3_interface.obj_size() > int(1e5):
        raise ValueError('initial_blind_split_handler(): config file is > 100kB. Make sure you uploaded the right file')
    s3_interface.s3_obj.download_file(local_key)

    # process settings
    s3_settings = S3Settings(local_key, 'SCITO')








def _create_main_queue(self):
    # main queue
    self.redrive_policy = {
        'deadLetterTargetArn': self.dead_letter_sqs.attributes['QueueArn'],
        'maxReceiveCount': self.settings.redrive_policy_max_receive_count
    }
    self.sqs.create_queue(QueueName=self.queue_name,
                          Attributes={'DelaySeconds': self.settings.delay_seconds,
                                      'KmsMasterKeyId': self.settings.kms_master_key_id,
                                      'RedrivePolicy': json.dumps(self.redrive_policy)})

def _create_dead_letter_queue(self):
    self.sqs.create_queue(QueueName=self.dead_letter_name,
                          Attributes={'DelaySeconds': self.settings.delay_seconds,
                                      'KmsMasterKeyId': self.settings.kms_master_key_id})




def activate_queue(self):
    if self.active_sqs != None:
        raise AttributeError('SQSInterface.activate_sqs(): there is an active queue in the instance attributes - '
                             f'{self.active_sqs.url}')
    self.active_sqs = self.sqs.get_queue_by_name(QueueName=self.queue_name)




def send_msg(self, msg_body):
    self.active_sqs.send_message(MessageBody=msg_body)

def scan_dead_letters(self):
    dead_letter_sqs = self.sqs.get_queue_by_name(QueueName=self.dead_letter_name)



def kill(self):
    try:
        self.activate_sqs()
    except AttributeError:
        pass
    attr_to_check = ['ApproximateNumberOfMessages',
                     'ApproximateNumberOfMessagesDelayed',
                     'ApproximateNumberOfMessagesNotVisible']
    pending_messages = [x for x in attr_to_check if self.active_sqs.attributes[x] != '0']
    if len(pending_messages) > 0:
        raise ValueError(f'SQSInterface.kill(): attempting to delete a queue with pending messages in {pending_messages}')
    self.active_sqs.delete()

