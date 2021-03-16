from scito_lambdas.lambda_utils import *
from scito_count.blind_byte_range import *
from scito_count.LambdaInterface import *
from io import StringIO

def main_handler(event: Dict, context) -> None:
    '''
    Function is triggered by an upload event. The downstream lambdas are created programmatically
    :param event: Dict. S3 records
    :param context:
    :return: None
    '''

    # id of this lambda
    lambda_name = 'genomics-blind-split'

    # config to buffer
    if len(event['Records']) > 1:
        raise ValueError('main_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    config_str = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    config_buf = config_sqs_import(config_str)

    # parse config
    config = init_config(config_buf)
    config_sections = config.keys()
    if len(config_sections) > 3:
        raise ValueError('main_handler(): current pipeline supports only technologies 3 FASTQ files per sample')

    # Create queues
    queue_name = construct_process_name(config, lambda_name)
    sqs_interface = SQSInterface(config, queue_name)
    if sqs_interface.queue_exists(dead_letter=True) | sqs_interface.queue_exists(dead_letter=False):
        raise SQSInterfaceError('main_handler(): SQS queues with provided names already exist')
    create_dead_letter_queue(sqs_interface)
    dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
    create_main_queue(sqs_interface, dead_letter.attributes['QueueArn'])
    main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)


    # Create lambda
    lambda_interface = LambdaInterface(config, lambda_name)
    if lambda_interface.function_exists():
        raise LambdaInterfaceError(f'main_handler(): function with the name {lambda_interface.lambda_name} already exists.')
    # TODO attach settings
    lambda_interface.aws_lambda.create_function(FunctionName=lambda_interface.lambda_name)


    lambda_interface.aws_lambda.create_event_source_mapping(EventSourceArn=main_queue.attributes['QueueArn'],
                                                            FunctionName=lambda_interface.lambda_name,
                                                            Enabled=True,
                                                            BatchSize=10)


    # sending messages to the queue per config section
    for section in config_sections:

        s3_settings = S3Settings(config, section)
        blind_ranges = blind_byte_range(s3_settings)

        # construct message
        msg_constant_part = {
            'config': config_str,
            'section': section,
            'byte_range': ''
        }
        [main_queue.send_message(MessageBody=finalize_message(msg_constant_part, x)) for x in blind_ranges]

