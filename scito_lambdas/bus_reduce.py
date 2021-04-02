from scito_lambdas.lambda_settings import settings_for_next_lambda
from scito_count.LambdaInterface import LambdaInterface
from scito_utils.factories import *
from scito_utils.S3InterfaceGen import *

import json
import subprocess as sp


def bus_reduce_handler(event):
    this_lambda_name = 'genomics-bus-reduce'
    previous_lambda_name = 'genomics-bus-constructor'

    if len(event['Records']) > 1:
        raise ValueError('bus_reduce_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    # get config
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    technology = extract_technology_config(config)

    # Destroy previous lambda
    lambda_interface = LambdaInterface(config=config, prefix=previous_lambda_name)
    lambda_interface.destroy()

    # get header for the BUS file to be constructed
    header = bit_header_factory(technology)
    outdir = settings_for_next_lambda(lambda_name='',
                                      settings_s3_key='anton/scito/scito_count/lambda_settings/bus_constructor_settings.json',
                                      dead_letter_arn='')['FileSystemConfigs']['LocalMountPath']

    # using select_files_to_sync function just to get the section of a ground truth file,
    # to keep naming consistent
    ground_section = select_files_to_sync(config)['ground']
    basename = os.path.basename(config[ground_section]['key']).split(".")[0]
    dirname = os.path.dirname(config[ground_section]['key'])
    outfile = os.path.join(outdir, dirname, f'{basename}.merged.bus')


    # for now try merge everything first then sort. IF performance is poor - try reduce operation
    regex = re.compile(f'{basename}.SORTED_BUS')
    sorted_bus_files = list(filter(regex.search, os.listdir(outdir)))
    with open(outfile, 'a') as f:
        f.write(header)
        for name_of_file in sorted_bus_files:
            sp.Popen(['tail', '-c', f'+{len(header) + 1}', name_of_file], stdout=f)

    # TODO delete parsed file

    gene_map = ...
    ec_map = ...
    tx_names = ...
    out_prefix = ...

    sp.Popen([f'bustools sort -T ./ -p - | bustools count -g {gene_map} -e {ec_map} -t {tx_names} '
              f'-o {out_prefix} --genecounts'], shell=True)

    # push outputs to s3
    bucket = config[ground_section]['bucket']
    bus_file_interface = S3Interface(bucket=bucket, object_key=outfile)
    bus_file_interface.s3_obj.upload_file(outfile)
    counts_interface = S3Interface(bucket=bucket, object_key=os.path.join(dirname, 'counts'))
    counts_interface.s3_obj.upload_file(out_prefix)

    # TODO push logs



