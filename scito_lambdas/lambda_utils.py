from urllib.parse import unquote_plus
from configparser import  ConfigParser
from typing import List, Tuple, Dict
import json

from scito_count.blind_byte_range import *
from scito_count.SQSInterface import *

def init_config(config_file: str) -> ConfigParser:
    '''

    :param config_file:
    :return:
    '''
    config_init = ConfigParser()
    config_init.read(config_file)
    return config_init

def bucket_key(record: Dict) -> Tuple:
    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    return s3_bucket, s3_key

def construct_s3_interface(s3_bucket: str, s3_key: str) -> S3Interface:
    s3_interface = S3Interface(s3_bucket, s3_key)
    if s3_interface.obj_size() > int(1e5):
        raise ValueError('initial_blind_split_handler(): config file is > 100kB. Make sure you uploaded the right file')
    return s3_interface



# TODO refactor this
def create_dead_letter_queue(sqs_interface: SQSInterface) -> None:
    sqs_interface.sqs.create_queue(QueueName=sqs_interface.dead_letter_name,
                                   Attributes={'DelaySeconds': sqs_interface.sqs_settings.delay_seconds,
                                               'KmsMasterKeyId': sqs_interface.sqs_settings.kms_master_key_id})


# TODO refactor this
def create_main_queue(sqs_interface: SQSInterface, dead_letter_arn: str) -> None:
    redrive_policy = {
        'deadLetterTargetArn': dead_letter_arn,
        'maxReceiveCount': sqs_interface.sqs_settings.maxReceiveCount
    }
    sqs_interface.sqs.create_queue(QueueName=sqs_interface.queue_name,
                                   Attributes={'DelaySeconds': sqs_interface.sqs_settings.delay_seconds,
                                               'KmsMasterKeyId': sqs_interface.sqs_settings.kms_master_key_id,
                                               'RedrivePolicy': json.dumps(redrive_policy)})

