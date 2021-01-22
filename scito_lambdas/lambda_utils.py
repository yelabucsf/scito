from urllib.parse import unquote_plus
from configparser import  ConfigParser
from typing import List, Tuple, Dict, Union
import json
from io import StringIO
from scito_count.blind_byte_range import *
from scito_count.SQSInterface import *

def init_config(config_file: Union[str, StringIO]) -> Dict:
    '''
    Initializes a config file
    :param config_file: Union[str, StringIO]. Location of a config file in a local filesystem, or a StringIO buffer
    :return: Dict
    '''
    config_init = ConfigParser()
    config_type = type(config_file).__name__
    if config_type == 'StringIO':
        config_init.read_file(config_file)
    elif config_type == 'str':
        config_init.read(config_file)
    else:
        raise ValueError(f'init_config(): {config_type} is not a supported input type')
    return dict(config_init._sections)


def bucket_key(record: Dict) -> Tuple:
    '''
    returns bucket name and object key for a record in the event triggered by S3 upload
    :param record: Dict. Single record in the event object
    :return: Tuple(str, str). S3 bucket and s3 object key
    '''
    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    return s3_bucket, s3_key

def construct_s3_interface(s3_bucket: str, s3_key: str) -> S3Interface:
    '''
    Constructs an S3Interface object
    :param s3_bucket: str
    :param s3_key: str
    :return: S3Interface object
    '''
    s3_interface = S3Interface(s3_bucket, s3_key)
    if s3_interface.obj_size() > int(1e5):
        raise ValueError('initial_blind_split_handler(): config file is > 100kB. Make sure you uploaded the right file')
    return s3_interface

def config_sqs_import(message: str) -> StringIO:
    config_buf = StringIO(message)
    config_buf.seek(0)
    return config_buf


def finalize_message(msg: Dict, blind_range: Tuple) -> str:
    msg['byte_range'] = f'{blind_range[0]}_{blind_range[1]}'
    finalized_msg = json.dumps(msg)
    return finalized_msg







# IMPURE FUNCTIONS - have side effects
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

