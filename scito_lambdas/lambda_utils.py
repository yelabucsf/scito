from urllib.parse import unquote_plus
from configparser import  ConfigParser
from typing import List, Tuple, Dict, Union, Type
import json
from io import StringIO
import re
import os

from scito_count.ContentTable import *
from scito_count.BitFile import *
from scito_count.SQSInterface import *
from scito_count.BlockCatalog import *
from scito_count.SeqFile import *

def init_config(config_file: Union[str, StringIO]) -> Dict:
    '''
    Initializes a config file
    :param config_file: Union[str, StringIO]. Location of a config file in a local filesystem, or a StringIO buffer
    :return: Dict. Config sections
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

def config_sqs_import(config_message: str) -> StringIO:
    config_buf = StringIO(config_message)
    config_buf.seek(0)
    return config_buf

def config_from_record(record: Dict) -> Dict:
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    config = init_config(config_buf)
    return config

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

def parse_range(byte_range: Union[Tuple, List, np.ndarray]) -> str:
    if len(byte_range) !=2:
        raise ValueError(f'parse_range(): byte range should contain only 2 values: start and end. Passed {len(byte_range)}')
    return f'{byte_range[0]}-{byte_range[1]}'


def finalize_message(msg: Dict, blind_range: Tuple) -> str:
    msg['byte_range'] = parse_range(blind_range)
    finalized_msg = json.dumps(msg)
    return finalized_msg

def que_name_from_arn(arn: str):
    deconstructed_arn = arn.split(':')
    return deconstructed_arn[-1]

def construct_process_name(config: Dict, prefix: str):
    '''
    constructs unique service name based on the processed FASTQ file name for Lambda and SQS - FOR ALL sections of the config
    :param config: str. FUll config.ini file in the form of Dict
    :param prefix: str. String representing current step (name of the lambda function)
    :return: str. Newly generated unique service name
    '''
    s3_key = list(config.values())[0]['key']
    key_base = s3_key.split('.')[0]
    split_key = key_base.split('/')[-2:]
    process_name = '_'.join([prefix]+split_key)
    return process_name

def origin_vs_expected_queue(record: Dict, previous_lambda: str) -> Tuple:
    config = config_from_record(record)
    origin_sqs_interface = SQSInterface(config, previous_lambda)
    origin_queue = que_name_from_arn(record['eventSourceARN'])
    expected_queue = origin_sqs_interface.queue_name
    return origin_queue, expected_queue


# IMPURE FUNCTIONS - have side effects
def create_queue(sqs_interface, use_dead_letter_arn: str=None):
    settings = {
        "QueueName": sqs_interface.dead_letter_name if use_dead_letter_arn == None else sqs_interface.queue_name,
        "Attributes": {
            "DelaySeconds": sqs_interface.sqs_settings.delay_seconds,
            "KmsMasterKeyId": sqs_interface.sqs_settings.kms_master_key_id
        }
    }
    if use_dead_letter_arn != None:
        settings["Attributes"]["RedrivePolicy"] = {
            'deadLetterTargetArn': use_dead_letter_arn,
            'maxReceiveCount': sqs_interface.sqs_settings.maxReceiveCount
        }
    sqs_interface.sqs.create_queue(**settings)