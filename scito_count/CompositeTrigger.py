class CompositeTrigger(object):
    def __init__(self, bucket: str, object_key: str):
        '''
        Class with information of an object in S3 bucket with input data. This object serves as a trigger for a Lambda
        function. If object is greater than 10 bytes, the lambda is triggered
        :param bucket:
        :param object_name:
        '''

        self._bucket = bucket
        pass