from scito_lambdas.lambda_utils import *
from scito_count.ContentTable import *


def catalog_build_handler(event, context):
    lambda_name = 'catalog-build'

    if len(event['Records']) > 1:
        raise ValueError('blind_split_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    # TODO pass the right event. For now it's an SQS message
    record_deconstructed = json.loads(record['body'])
    config_buf = config_sqs_import(record_deconstructed['config'])
    s3_settings = S3Settings(config_buf, record_deconstructed['section'])

    # import content tables from S3
    content_tables_io = ContentTablesIO(s3_settings)
    content_tables_io.content_table_stream()

    # produce content table with all BGZF ranges
    content_table = ContentTable(content_tables_io)




