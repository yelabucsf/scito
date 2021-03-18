from typing import Dict
class CompositeTrigger(object):
    def __init__(self, config: Dict, prefix: str):
        '''
        Class with information of an object in S3 bucket with input data. This object serves as a trigger for a Lambda
        function. If object is greater than 10 bytes, the lambda is triggered
        :param config: Dict.
        :param prefix: str.
        '''

        self._config = config
        self.size = 0
        self.complete = self._isComplete()
        pass

    def add_bytes(self):
        pass

    def _isComplete(self) -> bool:
        return len(self.size) >= 10