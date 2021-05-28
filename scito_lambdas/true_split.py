import json
from typing import Dict
from scito_count.BlocksIO import BlocksIO
from scito_count.BlockSplit import BlockSplit
from scito_count.SQSInterface import origin_vs_expected_queue
from scito_count.ProcessSettings import S3Settings
from scito_count.BlockByte import BlockByte
from scito_count.AWSExportIO import BlockByteExport
from scito_lambdas.architecture_utils import prepare_reduce_part


def true_split_record(record: Dict) -> None:
    # get config
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    s3_settings = S3Settings(config, parsed_record['section'])

    # find BGZF headers and construct byte ranges of inflatable BGZF parts
    byte_range = parsed_record['byte_range']
    handle = BlocksIO(s3_settings, byte_range)
    handle.get_object_part()
    block_split = BlockSplit(handle)
    block_byte = BlockByte(block_split)
    block_byte.byte_blocks()
    block_byte_export = BlockByteExport(s3_settings=s3_settings, misc_id=byte_range)
    block_byte_export.block_range_upload_s3(byte_seq=block_byte.byte_block_gen)


def true_split_handler(event):
    this_lambda_name = 'genomics-true-split'
    next_lambda_name = 'genomics-scito-catalog-build'

    # Check if origin queue is correct
    probe_record = event['Records'][0]
    origin_queue, expected_queue = origin_vs_expected_queue(probe_record, this_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    if len(event['Records']) > 10:
        raise ValueError('true_split_handler(): allowed lambda batch is up to 10 messages')
    [true_split_record(record) for record in event['Records']]

    # prepare reduce part
    prepare_reduce_part(record=probe_record, this_lambda_name=this_lambda_name, next_lambda_name=next_lambda_name)
