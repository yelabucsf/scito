from typing import Dict, Callable
import json

from scito_count.LambdaInterface import LambdaInterface, LambdaInterfaceError
from scito_count.SQSInterface import SQSInterface, problem_in_dead_letter_queue, SQSInterfaceError
from scito_lambdas.lambda_settings import settings_for_next_lambda, settings_event_source_true_split_lambda


# IMPURE FUNCTIONS - have side effects


def create_queues(sqs_interface, use_dead_letter_arn: str = None):
    settings = {
        "QueueName": sqs_interface.dead_letter_name if use_dead_letter_arn is None else sqs_interface.queue_name,
        "Attributes": {
            "KmsMasterKeyId": sqs_interface.sqs_settings['KmsMasterKeyId']
        }
    }
    if use_dead_letter_arn is not None:
        settings["Attributes"]["RedrivePolicy"] = json.dumps({
            'deadLetterTargetArn': use_dead_letter_arn,
            'maxReceiveCount': sqs_interface.sqs_settings['maxReceiveCount']
        })
    sqs_interface.sqs.create_queue(**settings)


def prep_queues(config: Dict, lambda_name: str):
    sqs_interface = SQSInterface(config=config, prefix=lambda_name)
    if sqs_interface.queue_exists(dead_letter=True) | sqs_interface.queue_exists(dead_letter=False):
        raise SQSInterfaceError('main_handler(): SQS queues with provided names already exist')
    create_queues(sqs_interface=sqs_interface, use_dead_letter_arn=None)  # Creates dead letter queue
    dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
    create_queues(sqs_interface=sqs_interface,
                  use_dead_letter_arn=dead_letter.attributes['QueueArn'])  # Creates main queue
    main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)
    return main_queue



# NOT TESTED
def prepare_reduce_part(record: Dict, next_lambda_name: str) -> None:
    """
    Impure function. Checks if there are messages pending. If the queue is empty it destroys it and invokes next lambda.
    If dead letter queue has messages - the error is thrown
    :param record: Dict. A record from a trigger event
    :param next_lambda_name: str. Name of the next lambda to invoke
    :return: None
    """
    # delete the main queue if it's empty
    parsed_record = json.loads(record['body'])
    config = json.loads(parsed_record['config'])
    origin_sqs_interface = SQSInterface(config=config, prefix=next_lambda_name)
    if not origin_sqs_interface.messages_pending(dead_letter=False):  # Is main queue empty
        if not origin_sqs_interface.messages_pending(dead_letter=True):  # Is dead letter queue empty
            origin_sqs_interface.destroy()
            next_lambda_interface = LambdaInterface(config=config, prefix='')
            payload = {'config': parsed_record['config']}
            next_lambda_interface.invoke_lambda(lambda_name=next_lambda_name, payload=json.dumps(payload))
        else:
            problem_in_dead_letter_queue(origin_sqs_interface)


def build_lambda(config: Dict, lambda_name: str, lambda_settings: str, event_source_func: Callable, sqs_queue) -> None:
    """
    Function to assemble lambda architectures for true_split and bus_constructor
    :param config: Dict. Config of the process
    :param lambda_name: str. Name of lambda function to create
    :param lambda_settings: str. S3 key to the settings JSON
    :param event_source_func: Callable. Function that creates event source mapping settings
    :param sqs_queue: SQSInterface.
    :return: 
    """
    lambda_interface = LambdaInterface(config, lambda_name)
    dead_letter_arn=json.loads(sqs_queue.attributes['RedrivePolicy'])['deadLetterTargetArn']
    if lambda_interface.function_exists():
        raise LambdaInterfaceError(
            f'main_handler(): function with the name {lambda_interface.lambda_name} already exists.')
    lambda_settings = settings_for_next_lambda(lambda_name=lambda_interface.lambda_name,
                                               settings_s3_key=lambda_settings,
                                               dead_letter_arn=dead_letter_arn)
    lambda_interface.aws_lambda.create_function(**lambda_settings)
    event_source_settings = event_source_func(sqs_queue.attributes['QueueArn'],
                                              lambda_interface.lambda_name)
    lambda_interface.aws_lambda.create_event_source_mapping(**event_source_settings)


def cleanup_protocol(config: Dict):
    lambda_names = ['genomics-true-split', 'genomics-bus-constructor']
    for lambda_name in lambda_names:
        lambda_interface = LambdaInterface(config, lambda_name)
        lambda_interface.destroy()
        sqs_interface = SQSInterface(config, lambda_name)
        sqs_interface.destroy()



