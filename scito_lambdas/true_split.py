from scito_count.BlocksIO import *
from scito_count.BlockSplit import *
from scito_lambdas.lambda_utils import *
from scito_count.AWSExportIO import *


# TODO refactor into smaller scopes
def true_split_record(record: Dict):
    previous_lambda = 'blind-split'

    # get config
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    config = init_config(config_buf)
    s3_settings = S3Settings(config, record_deconstructed['section'])

    # Check if origin queue is correct
    origin_sqs_interface = SQSInterface(config, previous_lambda)
    origin_queue = que_name_from_arn(record['eventSourceARN'])
    expected_queue = origin_sqs_interface.queue_name
    if expected_queue != origin_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    # find BGZF headers and construct byte ranges of inflatable BGZF parts
    byte_range = record_deconstructed['byte_range']
    handle = BlocksIO(s3_settings, byte_range)
    handle.get_object_part()
    block_split = BlockSplit(handle)
    block_byte = BlockByte(block_split)
    block_byte.byte_blocks()
    block_byte_export = BlockByteExport(s3_settings=s3_settings, misc_id='byte_range')
    block_byte_export.block_range_upload_s3(byte_seq=block_byte.byte_block_gen)


    # delete queues if they are empty
    # TODO build a logic to delete a queue
    active_queue = origin_sqs_interface.sqs.get_queue_by_name(QueueName=origin_sqs_interface.queue_name)
    active_queue.reload()


    # TODO Create next lambda





def true_split_handler(event, context):
    lambda_name = 'true-split'
    if len(event['Records']) > 10:
        raise ValueError('true_split_handler(): allowed lambda batch is up to 10 messages')
    for record in event:
        true_split_record(record)

