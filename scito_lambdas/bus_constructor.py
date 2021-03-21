from scito_count.SeqFile import FQFile
from scito_count.BUSTools import *
from scito_count.SQSInterface import *
from scito_count.LambdaInterface import LambdaInterface


def settings_for_sections(record: Dict) -> Dict:
    '''
    create a dict of settings per section.
    :param record: Dict
    :return: Dict{'section': Dict{s3, read, range}}
    '''
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

    settings = settings_for_sections(record)

    # TODO abstract. Make a factory
    # For now reads should be in order read2, read3
    # read sync
    reads = tuple(FQFile(settings[section]['s3_settings'],
                         settings[section]['read_settings'],
                         settings[section]['byte_range']) for section in settings)
    sync_two_reads = FQSyncTwoReads(reads)
    sync_two_reads.two_read_sync()

    # read arrange
    fixed_read2 = FQSeqArrangerAdtAtac(sync_two_reads)

    # create bus
    read3 = tuple(FQFile(settings[section]['s3_settings'],
                         settings[section]['read_settings'],
                         settings[section]['byte_range']) for section in settings)[-1]
    new_reads = (fixed_read2, read3)
    sync_two_reads = FQSyncTwoReads(new_reads)
    sync_two_reads.two_read_sync()

    bus_file_adt_atac = BUSFileAdtAtac(sync_two_reads)
    bus_file_adt_atac.bus_file_stream_adt_atac()
    adt_atac_bus_header = BUSHeaderAdtAtac()
    header = adt_atac_bus_header.output_header()
    native_bus_tools = BUSTools(bus_header=header, bus_records=bus_file_adt_atac.bit_records)
    native_bus_tools.run_pipe([native_bus_tools.bus_sort()])

    # export
    s3_set2 = ''  # TODO populate this
    outdir = ''  # TODO populate this
    bt_export = BUSToolsExport(s3_settings=s3_set2)
    bt_export.processed_bus_upload_efs(byte_seq=native_bus_tools.processed_bus_file, outdir=outdir)


def bus_constructor_handler(event, context):
    this_lambda_name = 'genomics-bus-constructor'
    previous_lambda_name = 'genomics-catalog-build'
    next_lambda_name = ''

    # Check if origin queue is correct
    probe_record = event['Records'][0]
    origin_queue, expected_queue = origin_vs_expected_queue(probe_record, previous_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    if len(event['Records']) > 2:
        raise ValueError('bus_constructor_handler(): allowed lambda batch is up to 2 messages')
    [bus_constructor_record(record) for record in event['Records']]

    # delete the main queue if it's empty
    parsed_record = json.loads(probe_record['body'])
    config = json.loads(parsed_record['config'])
    origin_sqs_interface = SQSInterface(config=config, prefix='previous_lambda_name')
    if not origin_sqs_interface.messages_pending(dead_letter=False):  # Is main queue empty
        if not origin_sqs_interface.messages_pending(dead_letter=True):  # Is dead letter queue empty
            origin_sqs_interface.destroy()
            next_lambda_interface = LambdaInterface(config=config, prefix='')
            payload = {'config': parsed_record['config']}
            next_lambda_interface.invoke_lambda(lambda_name=next_lambda_name, payload=json.dumps(payload))
        else:
            problem_in_dead_letter_queue(origin_sqs_interface)
