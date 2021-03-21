from scito_utils.factories import *

import json
import subprocess as sp


def bus_reduce_handler(event, context):
    this_lambda_name = 'genomics-bus-reduce'

    if len(event['Records']) > 1:
        raise ValueError('bus_reduce_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    # get config
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])

    # TODO get the tech
    header = bit_header_factory(tech)
    # TODO write the header to a file
    outfile = 'some_name'
    # TODO pass file name prefix
    list_of_names = []
    with open(outfile, 'a') as f:
        f.write(header)
        for name_of_file in list_of_names:
            sp.Popen(['tail', '-c', f'+{len(header) + 1}', name_of_file], stdout=f)

    # TODO delete parsed file

    gene_map = ...
    ec_map = ...
    tx_names = ...
    out_prefix = ...

    sp.Popen([f'bustools sort -T ./ -p - | bustools count -g {gene_map} -e {ec_map} -t {tx_names} '
              f'-o {out_prefix} --genecounts'], shell=True)

    #TODO outouts to the S3
