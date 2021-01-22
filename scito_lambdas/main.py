from scito_lambdas.lambda_utils import *
from io import StringIO



def main_handler(event, context):
    '''
    Function is triggered by an upload event. The downstream lambdas are created programmatically
    :param event:
    :param context:
    :return:
    '''

    # id of this lambda
    lambda_name = 'blind-split'

    # config to buffer
    if len(event['Records']) > 1:
        raise ValueError('blind_split_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    config_str = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    config_buf = StringIO(config_str)

    # parse config
    config_init = init_config(config_buf)
    config_sections = config_init.keys()
    if len(config_sections) > 3:
        raise ValueError('initial_blind_split_handler(): current pipeline supports only technologies 3 FASTQ files per sample')

    # sending messages to the queue per config section
    for section in config_sections:
        # !!!!!TODO create a lambda per each section

        s3_settings = S3Settings(config_buf, section)
        sqs_interface = SQSInterface(s3_settings, lambda_name)
        if not sqs_interface.queue_exists(dead_letter=True):
            create_dead_letter_queue(sqs_interface)
        dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
        if not sqs_interface.queue_exists(dead_letter=False):
            create_main_queue(sqs_interface, dead_letter.attributes['QueueArn'])
        main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)
        blind_ranges = blind_byte_range(s3_settings)

        # construct message
        msg_constant_part = {
            'config': config_str,
            'section': section,
            'byte_range': ''
        }
        [main_queue.send_message(MessageBody=finalize_message(msg_constant_part, x)) for x in blind_ranges]

