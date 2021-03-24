from scito_count.SeqFile import FQFile
from scito_count.BUSTools import *
from scito_count.SQSInterface import *
from scito_lambdas.lambda_settings import settings_for_bus_constructor_lambda


def settings_for_sections(record: Dict) -> Dict:
    '''
    create a dict of settings per section.
    :param record: Dict
    :return: Dict{'section': Dict{s3, read, range}}
    '''
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    ranges = json.loads(parsed_record['byte_range'])
    settings = {}
    for section in config.keys():
        settings[section] = {'s3_settings': S3Settings(config, section),
                             'read_settings': ReadSettings(config, section),
                             'byte_range': ranges[section]}
    return settings


def bus_constructor_record(record: Dict):
    settings = settings_for_sections(record)

    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    how_to_sync = select_files_to_sync(config)

    # TODO abstract. Make a factory
    # Arrange reads (stitch pool barcode to cell barcode)
    # read sync
    ground_read = FQFile(**settings[how_to_sync['ground']])
    async_read = FQFile(**settings[how_to_sync['async']])
    sync_two_reads = FQSyncTwoReads((ground_read, async_read))
    sync_two_reads.two_read_sync()

    # read arrange
    fixed_read = FQSeqArrangerAdtAtac(sync_two_reads)

    # read sync
    # create bus
    async_read = FQFile(**settings[how_to_sync['async']])  # instantiate again because it's a generator
    sync_two_reads = FQSyncTwoReads((fixed_read, async_read))
    sync_two_reads.two_read_sync()

    bus_file_adt_atac = BUSFileAdtAtac(sync_two_reads)
    bus_file_adt_atac.bus_file_stream_adt_atac()
    adt_atac_bus_header = BUSHeaderAdtAtac()
    header = adt_atac_bus_header.output_header()
    native_bus_tools = BUSTools(bus_header=header, bus_records=bus_file_adt_atac.bit_records)
    native_bus_tools.run_pipe([native_bus_tools.bus_sort()])

    # export
    export_settings = settings[how_to_sync['ground']]['s3_settings']
    outdir = settings_for_bus_constructor_lambda('')['FileSystemConfigs']['LocalMountPath']
    bt_export = BUSToolsExport(s3_settings=export_settings)
    bt_export.processed_bus_upload_efs(byte_seq=native_bus_tools.processed_bus_file, outdir=outdir)


def bus_constructor_handler(event, context):
    this_lambda_name = 'genomics-bus-constructor'
    previous_lambda_name = 'genomics-catalog-build'
    next_lambda_name = ''  # TODO add real arn or name

    # Check if origin queue is correct
    probe_record = event['Records'][0]
    origin_queue, expected_queue = origin_vs_expected_queue(probe_record, previous_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    if len(event['Records']) > 2:
        raise ValueError('bus_constructor_handler(): allowed lambda batch is up to 2 messages')
    [bus_constructor_record(record) for record in event['Records']]

    # prepare reduce part
    prepare_reduce_part(record=probe_record, service_prefix=previous_lambda_name, next_lambda_name=next_lambda_name)
