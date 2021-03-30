import boto3
from scito_count.ProcessSettings import *
from scito_lambdas.lambda_utils import construct_process_name


class LambdaInterfaceError(Exception):
    '''Errors corresponding to misuse of LambdaInterface'''


class LambdaInterface(object):
    def __init__(self, config: Dict, prefix: str, **kwargs):
        '''
        Abstraction to interact with a specific lambda based on the config
        :param config: Dict. Pipeline config imported as a dictionary
        :param prefix: str. Unique prefix for this process
        :param **kwargs: Dict. Kwargs for boto3.Session()
        '''
        session = boto3.Session(**kwargs)
        self.aws_lambda = session.client('lambda')
        self.lambda_name = construct_process_name(config, prefix)

    def function_exists(self) -> bool:
        try:
            current_function = self.aws_lambda.get_function(FunctionName=self.lambda_name)
        except self.aws_lambda.exceptions.ResourceNotFoundException:
            current_function = None
        return bool(current_function)

    def invoke_lambda(self, lambda_name: str, payload: str, **kwargs) -> Dict:
        invoke_settings = {
            "FunctionName": lambda_name,
            "InvocationType": "Event",
            "Payload": payload
        }
        invoke_settings.update(**kwargs)
        response = self.aws_lambda.invoke(**invoke_settings)
        return response

    def destroy(self):
        self.aws_lambda.delete_function(self.lambda_name)
