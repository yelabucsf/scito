from scito_lambdas.lambda_utils import *
from scito_count.BlockCatalog import *

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
    lambda_name = 'catalog-build'
    if len(event['Records']) > 1:
        raise ValueError('blind_split_handler(): trigger for this function should contain only a single record')

    record = event['Records'][0]

    # TODO pass the correct event. For now it's an SQS message
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    config = init_config(config_buf)
    catalogs = np.array([catalog_wrapper(config, x) for x in config.keys()]).T

    # Create queues
    queue_name = construct_process_name(config, lambda_name)
    sqs_interface = SQSInterface(config, queue_name)
    if sqs_interface.queue_exists(dead_letter=True) | sqs_interface.queue_exists(dead_letter=False):
        raise ValueError('main_handler(): SQS queues with provided names already exist')
    create_dead_letter_queue(sqs_interface)
    dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
    create_main_queue(sqs_interface, dead_letter.attributes['QueueArn'])
    main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)

    # TODO !!! Create Lambda

    # construct message
    msg_constant_part = {
        'config': record_deconstructed['config'],
        'byte_range': ''
    }

    for entry in catalogs:
        range_msg = catalog_parser(entry, config)
        msg_body = msg_constant_part.copy()
        msg_body['byte_range'] = range_msg
        main_queue.send_message(MessageBody=msg_body)
