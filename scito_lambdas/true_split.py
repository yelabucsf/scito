from scito_count.BlocksIO import *
from scito_count.BlockSplit import *
from scito_lambdas.lambda_utils import *


# TODO refactor into smaller scopes
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


def true_split_handler(event, context):
    previous_lambda_name = 'genomics-blind-split'
    this_lambda_name = 'genomics-true-split'
    next_lambda_name = ''

    # Check if origin queue is correct
    probe_record = event['Records'][0]
    origin_queue, expected_queue = origin_vs_expected_queue(probe_record, previous_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    # TODO check if lambda is correct

    if len(event['Records']) > 10:
        raise ValueError('true_split_handler(): allowed lambda batch is up to 10 messages')
    [true_split_record(record) for record in event['Records']]


    # delete the main queue if it's empty
    parsed_record = json.loads(probe_record['body'])
    config = json.loads(parsed_record['config'])
    origin_sqs_interface = SQSInterface(config=config, prefix='previous_lambda_name')
    if not origin_sqs_interface.messages_pending(dead_letter=False):    # Is main queue empty
        if not origin_sqs_interface.messages_pending(dead_letter=True): # Is dead letter queue empty
            origin_sqs_interface.destroy()
            next_lambda_interface = LambdaInterface(config=config, prefix='')
            payload = {'config': parsed_record['config']}
            next_lambda_interface.invoke_lambda(lambda_name='next_lambda_name', payload=json.dumps(payload))
        else:
            problem_in_dead_letter_queue(origin_sqs_interface)






