import boto3
import os
from scito_count.ProcessSettings import *

class LambdaInterface(object):
    def __init__(self, s3_settings, prefix):
        if s3_settings.profile == "":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=s3_settings.profile)
        self.aws_lambda = session.resource("lambda")
        self.lambda_name = '_'.join([prefix,
                                    os.path.basename(s3_settings.object_key).split(".")[0]])



        self.lambda_settings = {'DelaySeconds': '5',
                             'KmsMasterKeyId': 'alias/managed-sns-key',
                         'maxReceiveCount': '10'}