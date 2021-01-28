from scito_lambdas.lambda_utils import *
from scito_count.BitHeader import *

from io import BytesIO
import json



def bus_reduce_handler(event, context):
    lambda_name = 'bus-reduce'

    # TODO check if lambda is correct

    if len(event['Records']) > 1:
        raise ValueError('bus_reduce_handler(): trigger for this function should contain only a single record')

    record = event['Records'][0]

    # TODO pass the correct event. For now it's an SQS message
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    config = init_config(config_buf)

    # TODO pass file name prefix

