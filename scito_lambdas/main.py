from urllib.parse import unquote_plus

from scito_lambdas.lambda_utils import *
from scito_lambdas.architecture_utils import *
from scito_lambdas.lambda_settings import settings_for_next_lambda, settings_event_source_true_split_lambda, \
    settings_event_source_bus_constructor_lambda
from scito_count.SQSInterface import SQSInterface, SQSInterfaceError
from scito_count.blind_byte_range import *
from scito_count.LambdaInterface import *


def finalize_message(msg: Dict, blind_range: Tuple) -> str:
    msg['byte_range'] = parse_range(blind_range)
    finalized_msg = json.dumps(msg)
    return finalized_msg


def pipeline_config_s3(record: Dict) -> str:
    s3_bucket = record['s3']['bucket']['name']
    s3_key = unquote_plus(record['s3']['object']['key'])
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    config_str = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    return config_str


def config_for_main(event: Dict) -> Dict:

    if len(event['Records']) > 1:
        raise ValueError('main_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]
    config_str = pipeline_config_s3(record)
    config_buf = config_ini_to_buf(config_str)
    config = init_config(config_buf)
    if len(config.keys()) > 3:
        raise ValueError(
            'main_handler(): current pipeline supports only technologies with up to 3 FASTQ files per sample')
    return config


def build_dynamic_lambdas(config: Dict) -> None:
    lambda_names = ['genomics-true-split', 'genomics-bus-constructor']
    lambda_settings = ['true_split_settings.json',
                       'bus_constructor_settings.json']
    event_sources = [settings_event_source_true_split_lambda,
                     settings_event_source_bus_constructor_lambda]
    for architecture_blocks in zip(lambda_names, lambda_settings, event_sources):
        main_queue = prep_queues(config=config, lambda_name=architecture_blocks[0])
        this_lambda_settings = os.path.join('anton/scito/scito_count/lambda_settings/', architecture_blocks[1])
        build_lambda(config=config,
                     lambda_name=architecture_blocks,
                     lambda_settings=this_lambda_settings,
                     event_source_func=architecture_blocks[2],
                     sqs_queue=main_queue)




def main_handler(event: Dict) -> None:
    '''
    Function is triggered by an S3 upload event. The downstream lambdas are created or invoked programmatically
    :param event: Dict. S3 records
    :return: None
    '''

    # id of lambdas in concern
    next_lambda_name = 'genomics-true-split'

    # this config
    config = config_for_main(event)

    build_dynamic_lambdas(config)

    # activate SQS queue
    sqs_interface = SQSInterface(config, next_lambda_name)
    this_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)

    # sending messages to the queue per config section
    for section in config.keys():
        s3_settings = S3Settings(config, section)
        blind_ranges = blind_byte_range(s3_settings)

        # construct message
        msg_constant_part = {
            'section': section,
            'config': json.dumps(config),
            'byte_range': ''
        }
        [this_queue.send_message(MessageBody=finalize_message(msg_constant_part, x)) for x in blind_ranges]
