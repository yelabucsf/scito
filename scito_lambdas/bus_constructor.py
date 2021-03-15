from scito_lambdas.lambda_utils import *
from scito_count.BlockCatalog import *
from scito_count.SeqSync import *
from scito_count.SeqArranger import *
from scito_count.BitFile import *
from scito_count.BUSTools import *

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
    previous_lambda = 'genomics-catalog-build'

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
                         settings[section]['byte_range']) for section in settings)
    new_reads = (fixed_read2, read3)
    sync_two_reads = FQSyncTwoReads(new_reads)
    sync_two_reads.two_read_sync()

    bus_file_adt_atac = BUSFileAdtAtac(sync_two_reads)
    bus_file_adt_atac.bus_file_stream_adt_atac()
    adt_atac_bus_header = BUSHeaderAdtAtac()
    header = adt_atac_bus_header.output_header()
    native_bus_tools = BUSTools(bus_header=header, bus_records=bus_file_adt_atac.bit_records)
    native_bus_tools.run_pipe([native_bus_tools.bus_sort()])


    # TODO output to EFS


def bus_constructor_handler(event, context):
    lambda_name = 'genomics-bus-constructor'

    #TODO check if lambda is correct
    if len(event['Records']) > 2:
        raise ValueError('bus_constructor_handler(): allowed lambda batch is up to 2 messages')
    [bus_constructor_record(record) for record in event['Records']]