from scito_count.BlocksIO import *
from scito_count.BlockSplit import *
from scito_lambdas.lambda_utils import *
from scito_count.AWSExportIO import *
from scito_count.LambdaInterface import *


# TODO refactor into smaller scopes
def true_split_record(record: Dict) -> None:
    previous_lambda_name = 'genomics-blind-split'

    # get config
    parsed_record = json.loads(record['body'])
    config_buf = config_sqs_import(parsed_record['config'])
    config = init_config(config_buf)
    s3_settings = S3Settings(config, parsed_record['section'])

    # Check if origin queue is correct
    origin_queue, expected_queue = origin_vs_expected_queue(record, previous_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    # find BGZF headers and construct byte ranges of inflatable BGZF parts
    byte_range = parsed_record['byte_range']
    handle = BlocksIO(s3_settings, byte_range)
    handle.get_object_part()
    block_split = BlockSplit(handle)
    block_byte = BlockByte(block_split)
    block_byte.byte_blocks()
    block_byte_export = BlockByteExport(s3_settings=s3_settings, misc_id='byte_range')
    block_byte_export.block_range_upload_s3(byte_seq=block_byte.byte_block_gen)


    # delete queues if they are empty
    # TODO build a logic to delete a queue
    #active_queue = origin_sqs_interface.sqs.get_queue_by_name(QueueName=origin_sqs_interface.queue_name)
    #active_queue.reload()



def true_split_handler(event, context):
    this_lambda_name = 'genomics-true-split'
    # TODO check if lambda is correct

    if len(event['Records']) > 10:
        raise ValueError('true_split_handler(): allowed lambda batch is up to 10 messages')
    [true_split_record(record) for record in event['Records']]


