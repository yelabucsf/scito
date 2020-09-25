import boto3

class S3Interface(object):
    def __init__(self, bucket: str, object_key: str):
        self.s3 = boto3.resource("S3")
        self.full_name = self.s3.Object(bucket, object_key)



