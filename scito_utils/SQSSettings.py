# Keep as a class for now

class SQSSettings(object):
    def __init__(self):
        self.delay_seconds = '5'
        self.kms_master_key_id = 'alias/managed-sns-key'
        self.redrive_policy_max_receive_count = '10'
