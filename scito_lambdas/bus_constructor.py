from scito_lambdas.lambda_utils import *
from scito_count.BlockCatalog import *

def settings_for_sections(record: Dict) -> Dict:
    record_deconstructed = json.loads(record['body'])
    config = config_from_record(record)
    ranges = json.loads(record_deconstructed['byte_range'])
    settings = {}
    for section in config.keys():
        settings[section] = {'s3_settings': S3Settings(config, section),
                             'read_settings': ReadSettings(config, section),
                             'byte_range': ranges[section]}
    return settings



def bus_constructor_record(record: Dict):
    previous_lambda = 'catalog-build'

    # get config
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    config = init_config(config_buf)

    # Check if origin queue is correct
    origin_queue, expected_queue = origin_vs_expected_queue(record, previous_lambda)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    settings = settings_for_sections(record)

    # TODO abstract
    # read arranger
    read_dict = {section: FQFile(settings[section]['s3_settings'],
                                 settings[section]['read_settings'],
                                 settings[section]['byte_range']) for section in settings}


    # construct dict of S3Settings


def bus_constructor_handler(event, context):
    pass