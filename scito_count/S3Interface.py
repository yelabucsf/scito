import boto3


class S3Interface(object):
    def __init__(self, bucket: str, object_key: str, **kwargs):
        session = boto3.Session(**kwargs)
        s3 = session.resource('s3')
        self.s3_obj = s3.Object(bucket, object_key)
        self.bucket = s3.Bucket(bucket)

    def obj_size(self):
        return self.s3_obj.content_length

    def get_bytes_s3(self, start, end):
        return self.s3_obj.get(Range=f"bytes={start}-{end}")["Body"]

    def filter_objects(self, prefix):
        return self.bucket.objects.filter(Prefix=prefix)
