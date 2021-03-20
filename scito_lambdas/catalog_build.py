from scito_lambdas.lambda_utils import *
from scito_count.BlockCatalog import *
from scito_count.LambdaInterface import *
from scito_count.ContentTable import *

### HARDCODED SETTINGS
# Kinda hardcoded function to get settings for the next lambda from S3
def settings_for_bus_constructor_lambda(lambda_name: str) -> Dict:
    s3_bucket = ''
    s3_key = ''
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    try:
        settings_from_s3 = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    except:
        raise ValueError('settings_for_bus_constructor_lambda(): settings for true_split_lambda do not exist. Contact the '
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
        "BatchSize": 2,
        "MaximumBatchingWindowInSeconds": 20
    }
    return settings
## END hardcoded


def catalog_wrapper(config: Dict, section: str):
    s3_settings = S3Settings(config, section)
    content_tables_io = ContentTablesIO(s3_settings)
    content_tables_io.content_table_stream()
    content_table = ContentTable(content_tables_io)
    block_catalog = BlockCatalog(n_parts=8000) # magic number targeting 2**13 lambda processes

    # TODO logic for overlap
    block_catalog.create_catalog(content_table=content_table.content_table_arr, overlap=overlap)
    return block_catalog

def catalog_parser(sync_ranges, config: Dict) -> str:
    '''
    Constructs a part of SQS message corresponding to Dict{'section': 'start-end'}
    :param sync_ranges: np.ndarray. numpy array of catalogs with dim (n_sections, 2)
    :param config: Dict. Process config
    :return: str.
    '''
    if len(sync_ranges) != len(config.keys()):
        raise ValueError(f'catalog_parser(): number of FASTQ files: {len(config.keys())} does not match number '
                         f'of passed byte ranges {len(sync_ranges)}')
    str_ranges = [parse_range(x) for x in sync_ranges]
    return json.dumps(dict(zip(config.keys(), str_ranges)))



def catalog_build_handler(event, context):
    this_lambda_name = 'genomics-catalog-build'
    next_lambda_name = 'genomics-bus-constructor'

    # config to buffer
    if len(event['Records']) > 1:
        raise ValueError('catalog_build_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    # get config
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])

    catalogs = np.array([catalog_wrapper(config, x) for x in config.keys()]).T

    # Create queues
    queue_name = construct_process_name(config, this_lambda_name)
    sqs_interface = SQSInterface(config, queue_name)
    if sqs_interface.queue_exists(dead_letter=True) | sqs_interface.queue_exists(dead_letter=False):
        raise ValueError('main_handler(): SQS queues with provided names already exist')
    main_queue = prep_queue(sqs_interface)


    # Create lambda
    lambda_interface = LambdaInterface(config, next_lambda_name)
    if lambda_interface.function_exists():
        raise LambdaInterfaceError(f'main_handler(): function with the name {lambda_interface.lambda_name} already exists.')

    # ingest lambda settings
    next_lambda_settings = settings_for_bus_constructor_lambda(lambda_interface.lambda_name)
    lambda_interface.aws_lambda.create_function(**next_lambda_settings)

    event_source_settings = settings_event_source(main_queue.attributes['QueueArn'], lambda_interface.lambda_name)
    lambda_interface.aws_lambda.create_event_source_mapping(**event_source_settings)


    # construct message
    msg_constant_part = {
        'config': parsed_record['config'],
        'byte_range': ''
    }

    for entry in catalogs:
        range_msg = catalog_parser(entry, config)
        msg_body = msg_constant_part.copy()
        msg_body['byte_range'] = range_msg
        main_queue.send_message(MessageBody=msg_body)
