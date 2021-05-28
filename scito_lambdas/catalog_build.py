import json
import numpy as np

from typing import Dict
from scito_lambdas.lambda_utils import parse_range
from scito_count.ProcessSettings import S3Settings
from scito_count.ContentTablesIO import ContentTablesIO
from scito_count.SQSInterface import SQSInterface
from scito_count.BlockCatalog import BlockCatalog, define_overlap
from scito_count.LambdaInterface import LambdaInterface
from scito_count.ContentTable import ContentTable


def catalog_wrapper(config: Dict, section: str):
    s3_settings = S3Settings(config, section)
    content_tables_io = ContentTablesIO(s3_settings)
    content_tables_io.content_table_stream()
    content_table = ContentTable(content_tables_io)
    block_catalog = BlockCatalog(n_parts=8000)  # magic number targeting 2**13 lambda processes

    overlap = define_overlap(config, section)
    block_catalog.create_catalog(content_table=content_table.content_table_arr, overlap=overlap)
    return block_catalog


def catalog_parser(sync_ranges, config: Dict) -> str:
    """
    Constructs a part of SQS message corresponding to Dict{'section': 'start-end'}
    :param sync_ranges: np.ndarray. numpy array of catalogs with dim (n_sections, 2)
    :param config: Dict. Process config
    :return: str.
    """
    if len(sync_ranges) != len(config.keys()):
        raise ValueError(f'catalog_parser(): number of FASTQ files: {len(config.keys())} does not match number '
                         f'of passed byte ranges {len(sync_ranges)}')
    str_ranges = [parse_range(x) for x in sync_ranges]
    return json.dumps(dict(zip(config.keys(), str_ranges)))


def catalog_build_handler(event):
    next_lambda_name = 'genomics-bus-constructor'
    previous_lambda_name = 'genomics-true-split'

    # config to buffer
    if len(event['Records']) > 1:
        raise ValueError('catalog_build_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    # get config
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])

    # Destroy previous lambda
    lambda_interface = LambdaInterface(config=config, prefix=previous_lambda_name)
    lambda_interface.destroy()

    catalogs = np.array([catalog_wrapper(config, x) for x in config.keys()]).T

    # activate SQS queue
    sqs_interface = SQSInterface(config, next_lambda_name)
    this_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)

    # construct message
    msg_constant_part = {
        'config': parsed_record['config'],
        'byte_range': ''
    }

    for entry in catalogs:
        range_msg = catalog_parser(entry, config)
        msg_body = msg_constant_part.copy()
        msg_body['byte_range'] = range_msg
        this_queue.send_message(MessageBody=msg_body)
