def true_split_record(record):
    pass


def true_split_handler(event, context):
    if len(event['Records']) > 10:
        raise ValueError('true_split_handler(): allowed lambda batch is up to 10 messages')

