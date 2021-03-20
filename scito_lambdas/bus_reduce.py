from scito_lambdas.lambda_utils import *
from scito_count.BitHeader import *
from scito_utils.factories import *

from io import BytesIO
import json
import subprocess as sp


def bus_reduce_handler(event, context):
    this_lambda_name = 'genomics-bus-reduce'

    # TODO check if lambda is correct

    if len(event['Records']) > 1:
        raise ValueError('bus_reduce_handler(): trigger for this function should contain only a single record')

    record = event['Records'][0]

    # TODO pass the correct event. For now it's an SQS message
    record_deconstructed = json.loads(record['body'])
    config_buf = config_ini_to_buf(record_deconstructed['config'])
    config = init_config(config_buf)

    # ToDo get the tech
    header = bit_header_factory(tech)
    # TODO write the header to a file
    outfile = 'some_name'
    # TODO pass file name prefix
    list_of_names = []
    with open(outfile, 'a') as f:
        f.write(header)
        for name_of_file in list_of_names:
            sp.Popen(['tail', '-c', f'+{len(header)+1}', name_of_file], stdout=f)

    gene_map = ...
    ec_map = ...
    tx_names = ...

    sp.Popen([f'bustools sort -T ./ -p - | bustools count {gene_map} {ec_map} {tx_names}'], shell=True)









