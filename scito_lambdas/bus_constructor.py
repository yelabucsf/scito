import json
from typing import Dict
from scito_count.BUSTools import BUSTools
from scito_count.AWSExportIO import BUSToolsExport
from scito_count.SQSInterface import origin_vs_expected_queue
from scito_lambdas.lambda_settings import settings_for_next_lambda
from scito_lambdas.lambda_utils import extract_technology_config
from scito_lambdas.architecture_utils import prepare_reduce_part
from scito_count.ProcessSettings import S3Settings, ReadSettings
from scito_count.SeqSync import select_files_to_sync
from scito_utils.factories import seq_file_factory, seq_sync_factory, seq_arranger_factory, \
    bit_file_factory, bit_header_factory


def settings_for_sections(record: Dict) -> Dict:
    """
    create a dict of settings per section.
    :param record: Dict
    :return: Dict{'section': Dict{s3, read, range}}
    """
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    ranges = json.loads(parsed_record['byte_range'])
    settings = {}
    for section in config.keys():
        settings[section] = {'s3_settings': S3Settings(config, section),
                             'read_settings': ReadSettings(config, section),
                             'byte_range': ranges[section]}
    return settings


def bus_constructor_record(record: Dict, outdir: str):
    settings = settings_for_sections(record)

    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    how_to_sync = select_files_to_sync(config)

    # Arrange reads (stitch pool barcode to cell barcode)
    # read sync
    technology = extract_technology_config(config)
    ground_read = seq_file_factory(technology)(**settings[how_to_sync['ground']])
    async_read = seq_file_factory(technology)(**settings[how_to_sync['async']])
    sync_two_reads = seq_sync_factory(technology)((ground_read, async_read))
    sync_two_reads.two_read_sync()

    fixed_read = seq_arranger_factory(technology)(sync_two_reads)

    # instantiate again because it's a generator
    async_read = seq_file_factory(technology)(**settings[how_to_sync['async']])
    sync_two_reads = seq_sync_factory(technology)((fixed_read, async_read))
    sync_two_reads.two_read_sync()

    bus_file = bit_file_factory(technology)(sync_two_reads)
    bus_file.bus_file_stream()
    header = bit_header_factory(technology)
    native_bus_tools = BUSTools(bus_header=header, bus_records=bus_file.bit_records)
    native_bus_tools.run_pipe([native_bus_tools.bus_sort()])

    # export
    export_settings = settings[how_to_sync['ground']]['s3_settings']
    bt_export = BUSToolsExport(s3_settings=export_settings)
    bt_export.processed_bus_upload_efs(byte_seq=native_bus_tools.processed_bus_file, outdir=outdir)


def bus_constructor_handler(event):
    this_lambda_name = 'genomics-bus-constructor'
    next_lambda_name = 'genomics-bus-reduce'

    outdir = settings_for_next_lambda(
        lambda_name='',
        settings_s3_key='anton/scito/scito_count/lambda_settings/bus_constructor_settings.json',
        dead_letter_arn=''
    )['FileSystemConfigs']['LocalMountPath']

    # Check if origin queue is correct
    probe_record = event['Records'][0]
    origin_queue, expected_queue = origin_vs_expected_queue(probe_record, this_lambda_name)
    if origin_queue != expected_queue:
        raise ValueError('true_split_record(): receiving messages from unknown SQS queue: '
                         f'expecting from {expected_queue}, receiving from {origin_queue}')

    if len(event['Records']) > 2:
        raise ValueError('bus_constructor_handler(): allowed lambda batch is up to 2 messages')
    [bus_constructor_record(record=record, outdir=outdir) for record in event['Records']]

    # prepare reduce part
    prepare_reduce_part(record=probe_record, this_lambda_name=this_lambda_name, next_lambda_name=next_lambda_name)
