from configparser import ConfigParser
from typing import Union, Dict, Tuple, List
import json
from scito_count.AWSExportIO import *
from io import StringIO
import numpy as np


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


def config_ini_to_buf(config_message: str) -> StringIO:
    config_buf = StringIO(config_message)
    config_buf.seek(0)
    return config_buf


def parse_range(byte_range: Union[Tuple, List, np.ndarray]) -> str:
    if len(byte_range) != 2:
        raise ValueError(
            f'parse_range(): byte range should contain only 2 values: start and end. Passed {len(byte_range)}')
    return f'{byte_range[0]}-{byte_range[1]}'


def construct_process_name(config: Dict, prefix: str) -> str:
    '''
    constructs unique service name based on the processed FASTQ file name for Lambda and SQS - FOR ALL sections of
    the config
    :param config: str. FUll config.ini file in the form of Dict
    :param prefix: str. String representing
    current step (name of the lambda function) :return: str. Newly generated unique service name
    '''
    s3_key = list(config.values())[0]['key']
    key_base = s3_key.split('.')[0]
    split_key = key_base.split('/')[-2:]
    process_name = '_'.join([prefix] + split_key)
    return process_name


def extract_technology_config(config: Dict) -> str:
    current_technology = [config[x]['technology'] for x in config]
    if len(set(current_technology)) > 1:
        raise ValueError(f'select_files_to_sync(): Detected multiple technologies in the config file.'
                         f'Specified technologies are {set(current_technology)}. Specify only one type of technology')
    else:
        return current_technology[0]


