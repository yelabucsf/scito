from scito_lambdas.lambda_utils import *

def blind_split_handler(event, context):

    # id of this lambda
    lambda_name = 'blind-split'

    # download config
    if len(event['Records']) > 1:
        raise ValueError('blind_split_handler(): trigger for this function should contain only a single record')
    record = event['Records'][0]

    s3_bucket, s3_key = bucket_key(record)
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    local_key = s3_key.replace('/', '_')
    s3_interface.s3_obj.download_file(local_key)

    # parse config
    config_init = init_config(local_key)
    config_sections = config_init.sections()
    if len(config_sections) > 3:
        raise ValueError('initial_blind_split_handler(): current pipeline supports only technologies 3 FASTQ files per sample')

    # sending messages to the queue per config section
    for section in config_sections:
        s3_settings = S3Settings(local_key, section)
        sqs_interface = SQSInterface(s3_settings, lambda_name)
        if not sqs_interface.queue_exists(dead_letter=True):
            create_dead_letter_queue(sqs_interface)
        dead_letter = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.dead_letter_name)
        if not sqs_interface.queue_exists(dead_letter=False):
            create_main_queue(sqs_interface, dead_letter.attributes['QueueArn'])
        main_queue = sqs_interface.sqs.get_queue_by_name(QueueName=sqs_interface.queue_name)

        blind_ranges = blind_byte_range(s3_settings)
        [main_queue.send_message(MessageBody=f'{x[0]}_{x[1]}') for x in blind_ranges]























def activate_queue(self):
    if self.active_sqs != None:
        raise AttributeError('SQSInterface.activate_sqs(): there is an active queue in the instance attributes - '
                             f'{self.active_sqs.url}')
    self.active_sqs = self.sqs.get_queue_by_name(QueueName=self.queue_name)




def send_msg(self, msg_body):
    self.active_sqs.send_message(MessageBody=msg_body)






