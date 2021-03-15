import boto3
import os
from typing import Dict
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import construct_process_name

class LambdaInterface(object):
    def __init__(self, config: Dict, prefix: str):
        s3_settings = S3Settings(config, list(config.keys())[0])
        if s3_settings.profile == "":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=s3_settings.profile)
        self.aws_lambda = session.resource("lambda")
        self.lambda_name = construct_process_name(config, prefix)

    def function_exists(self):
        try:
            current_function = self.aws_lambda.get_function(self.lambda_name)
        except self.aws_lambda.exceptions.ResourceNotFoundException:
            current_function = None
        return bool(current_function)




