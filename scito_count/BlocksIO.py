from scito_count.BlockSplit import *
from scito_count.BlockCatalog import *
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *
from scito_count.SeqExport import *
from scito_count.BlockByte import *
from io import BytesIO
import os

'''
Class to import ranges of bytes from s3 directly to RAM
'''

class BlocksIO(object):
    __slots__ = 'block_start', 'block_end', 's3_interface', 'data_stream'
    def __init__(self, s3_settings: S3Settings, byte_range: str):
        '''
        :param byte_range: comes from an SQS. Format "start-end"
        '''
        self.block_start, self.block_end = [int(x) for x in byte_range.split("-")]
        self.s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
        self.data_stream = BytesIO()

    def get_object_part(self):
        self.data_stream.write(self.s3_interface.get_bytes_s3(self.block_start, self.block_end).read())
        self.data_stream.seek(0)

    def close(self):
        self.data_stream.close()








