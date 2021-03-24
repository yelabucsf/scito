from typing import Dict
import json

from scito_count.LambdaInterface import LambdaInterface
from scito_count.SQSInterface import SQSInterface, problem_in_dead_letter_queue

# NOT TESTED
# IMPURE FUNCTIONS - have side effects
def create_queues(sqs_interface, use_dead_letter_arn: str = None):
    settings = {
        "QueueName": sqs_interface.dead_letter_name if use_dead_letter_arn is None else sqs_interface.queue_name,
        "Attributes": {
            "DelaySeconds": sqs_interface.sqs_settings.delay_seconds,
            "KmsMasterKeyId": sqs_interface.sqs_settings.kms_master_key_id
        }
    }
    if use_dead_letter_arn is not None:
        settings["Attributes"]["RedrivePolicy"] = {
            'deadLetterTargetArn': use_dead_letter_arn,
            'maxReceiveCount': sqs_interface.sqs_settings.maxReceiveCount
        }
    sqs_interface.sqs.create_queue(**settings)


def prep_queues(sqs_interface):
    create_queues(sqs_interface=sqs_interface, use_dead_letter_arn=None)  # Creates dead letter queue
    dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
    create_queues(sqs_interface=sqs_interface,
                  use_dead_letter_arn=dead_letter.attributes['QueueArn'])  # Creates main queue
    main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)
    return main_queue


def prepare_reduce_part(record: Dict, service_prefix: str, next_lambda_name: str) -> None:
    '''
    Impure function. Checks if there are messages pending. If the queue is empty it destroys it and invokes next lambda.
    If dead letter queue has messages - the error is thrown
    :param record: Dict. A record from a trigger event
    :param service_prefix: str. Previous lambda name to check a correct queue
    :param next_lambda_name: str. Name of the next lambda to invoke
    :return: None
    '''
    # delete the main queue if it's empty
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    origin_sqs_interface = SQSInterface(config=config, prefix=service_prefix)
    if not origin_sqs_interface.messages_pending(dead_letter=False):  # Is main queue empty
        if not origin_sqs_interface.messages_pending(dead_letter=True):  # Is dead letter queue empty
            origin_sqs_interface.destroy()
            next_lambda_interface = LambdaInterface(config=config, prefix='')
            payload = {'config': parsed_record['config']}
            next_lambda_interface.invoke_lambda(lambda_name=next_lambda_name, payload=json.dumps(payload))
        else:
            problem_in_dead_letter_queue(origin_sqs_interface)
