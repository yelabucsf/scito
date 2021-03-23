from scito_lambdas.lambda_utils import *

# Kinda hardcoded function to get settings for the next lambda from S3
# HARDCODED SETTINGS FOR true_split FUNCTION
def settings_for_true_split_lambda(lambda_name: str) -> Dict:
    s3_bucket = 'ucsf-genomics-prod-project-data'
    s3_key = 'anton/scito/scito_count/true_split_settings.json'
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    try:
        settings_from_s3 = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    except:
        raise ValueError('settings_for_true_split_lambda(): settings for true_split_lambda do not exist. Contact the '
                         'admin of this pipeline')
    lambda_settings = json.loads(settings_from_s3)
    lambda_settings["FunctionName"] = lambda_name
    return lambda_settings


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
def settings_for_bus_constructor_lambda(lambda_name: str) -> Dict:
    s3_bucket = 'ucsf-genomics-prod-project-data'
    s3_key = 'anton/scito/scito_count/bus_constructor_settings.json'
    s3_interface = construct_s3_interface(s3_bucket, s3_key)
    try:
        settings_from_s3 = s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
    except:
        raise ValueError(
            'settings_for_bus_constructor_lambda(): settings for true_split_lambda do not exist. Contact the '
            'admin of this pipeline')
    lambda_settings = json.loads(settings_from_s3)
    lambda_settings["FunctionName"] = lambda_name
    return lambda_settings


# Kinda hardcoded function to get settings for the resource mapping for the next lambda
def settings_event_source_bus_constructor_lambda(event_source_arn: str, lambda_name: str):
    settings = {
        "EventSourceArn": event_source_arn,
        "FunctionName": lambda_name,
        "Enabled": True,
        "BatchSize": 2,
        "MaximumBatchingWindowInSeconds": 20
    }
    return settings
