import boto3
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import construct_process_name


class LambdaInterfaceError(Exception):
    '''Errors corresponding to misuse of LambdaInterface'''


class LambdaInterface(object):
    def __init__(self, config: Dict, prefix: str):
        '''
        Abstraction to interact with a specific lambda based on the config
        :param config: Dict. Pipeline config imported as a dictionary
        :param prefix: str. Unique prefix for this process
        '''
        s3_settings = S3Settings(config, list(config.keys())[0])
        if s3_settings.profile == "":
            session = boto3.Session()
        else:
            session = boto3.Session(profile_name=s3_settings.profile)
        self.aws_lambda = session.resource("lambda")
        self.lambda_name = construct_process_name(config, prefix)

    def function_exists(self) -> bool:
        try:
            current_function = self.aws_lambda.get_function(self.lambda_name)
        except self.aws_lambda.exceptions.ResourceNotFoundException:
            current_function = None
        return bool(current_function)

    def invoke_lambda(self, lambda_name: str, payload: str) -> Dict:
        invoke_settings = {
            "FunctionName": lambda_name,
            "InvocationType": "Event",
            "Payload": payload
        }
        response = self.aws_lambda.invoke(**invoke_settings)
        return response
