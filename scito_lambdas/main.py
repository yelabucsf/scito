from urllib.parse import unquote_plus

from scito_count.SQSInterface import SQSInterface, SQSInterfaceError
from scito_lambdas.lambda_utils import *
from scito_count.blind_byte_range import *
from scito_count.LambdaInterface import *


# HARDCODED SETTINGS
# Kinda hardcoded function to get settings for the next lambda from S3
def settings_for_true_split_lambda(lambda_name: str) -> Dict:
    s3_bucket = 'ucsf-genomics-prod-project-data'
    s3_key = 'anton/scito/scito_count/true_split_settings.json'
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    try:
        settings_from_s3 = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    except:
        raise ValueError('settings_for_true_split_lambda(): settings for true_split_lambda do not exist. Contact the '
                         'admin of this pipeline')
    lambda_settings = json.loads(settings_from_s3)
    lambda_settings["FunctionName"] = lambda_name
    return lambda_settings


# Kinda hardcoded function to get settings for the resource mapping for the next lambda
def settings_event_source(event_source_arn: str, lambda_name: str):
    settings = {
        "EventSourceArn": event_source_arn,
        "FunctionName": lambda_name,
        "Enabled": True,
        "BatchSize": 10,
        "MaximumBatchingWindowInSeconds": 20
    }
    return settings

# END hardcoded

def pipeline_config_s3(record: Dict) -> str:
    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    config_str = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    return config_str


def main_handler(event: Dict, context) -> None:
    '''
    Function is triggered by an S3 upload event. The downstream lambdas are created or invoked programmatically
    :param event: Dict. S3 records
    :param context:
    :return: None
    '''

    # id of lambdas in concern
    this_lambda_name = 'genomics-blind-split'
    next_lambda_name = 'genomics-true-split'

    # config to buffer
    if len(event['Records']) > 1:
        raise ValueError('main_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    config_str = pipeline_config_s3(record)

    # parse config
    config_buf = config_ini_to_buf(config_str)
    config = init_config(config_buf)
    config_sections = config.keys()
    if len(config_sections) > 3:
        raise ValueError(
            'main_handler(): current pipeline supports only technologies with up to 3 FASTQ files per sample')

    # Create queues
    sqs_interface = SQSInterface(config, this_lambda_name)
    if sqs_interface.queue_exists(dead_letter=True) | sqs_interface.queue_exists(dead_letter=False):
        raise SQSInterfaceError('main_handler(): SQS queues with provided names already exist')
    main_queue = prep_queue(sqs_interface)

    # Create lambda
    lambda_interface = LambdaInterface(config, next_lambda_name)
    if lambda_interface.function_exists():
        raise LambdaInterfaceError(
            f'main_handler(): function with the name {lambda_interface.lambda_name} already exists.')

    # ingest lambda settings
    next_lambda_settings = settings_for_true_split_lambda(lambda_interface.lambda_name)
    lambda_interface.aws_lambda.create_function(**next_lambda_settings)

    event_source_settings = settings_event_source(main_queue.attributes['QueueArn'], lambda_interface.lambda_name)
    lambda_interface.aws_lambda.create_event_source_mapping(**event_source_settings)

    # sending messages to the queue per config section
    for section in config_sections:
        s3_settings = S3Settings(config, section)
        blind_ranges = blind_byte_range(s3_settings)

        # construct message
        msg_constant_part = {
            'section': section,
            'config': json.dumps(config),
            'byte_range': ''
        }
        [main_queue.send_message(MessageBody=finalize_message(msg_constant_part, x)) for x in blind_ranges]
