from scito_lambdas.lambda_utils import *


# Kinda hardcoded function to get settings for the next lambda from S3
def settings_for_next_lambda(lambda_name: str, settings_s3_key: str, dead_letter_arn: str, **kwargs) -> Dict:
    s3_bucket = 'ucsf-genomics-prod-project-data'
    s3_interface = construct_s3_interface(s3_bucket, settings_s3_key)
    try:
        settings_from_s3 = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    except:
        raise ValueError('settings_for_true_split_lambda(): settings for true_split_lambda do not exist. Contact the '
                         'admin of this pipeline')
    lambda_settings = json.loads(settings_from_s3)
    lambda_settings.update({"FunctionName": lambda_name,
                            "DeadLetterConfig": {
                                "TargetArn": dead_letter_arn
                            }})
    lambda_settings.update(**kwargs)
    return lambda_settings


# Hardcoded for event mapping
# HARDCODED SETTINGS FOR true_split FUNCTION
def settings_event_source_true_split_lambda(event_source_arn: str, lambda_name: str):
    settings = {
        "EventSourceArn": event_source_arn,
        "FunctionName": lambda_name,
        "Enabled": True,
        "BatchSize": 10,
        "MaximumBatchingWindowInSeconds": 20
    }
    return settings


# HARDCODED SETTINGS FOR bus_constructor FUNCTION
def settings_event_source_bus_constructor_lambda(event_source_arn: str, lambda_name: str):
    settings = {
        "EventSourceArn": event_source_arn,
        "FunctionName": lambda_name,
        "Enabled": True,
        "BatchSize": 2,
        "MaximumBatchingWindowInSeconds": 20
    }
    return settings
