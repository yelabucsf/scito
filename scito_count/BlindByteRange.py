import subprocess as sp
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *

'''
Class produces a blind catalog of large files producing a range of 5 Gb + 18 bytes (to avoid BGZF header split)
This is done because files > 12 Gb take over 1 min to get proper BlockCatalog, which is not suitable for lambda.
Target - get files down to 5 Gb.
'''
class BlindByteRange(object):
    def __init__(self, s3_settings: S3Settings):
        self.s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
        obj_size = self.s3_interface.obj_size()
        window_start = 0
        while (window_start + int(5e9)) < obj_size:
            window_end = window_start + int(5e9)
            window_start += window_end - 18 # 18 bytes is the BGZF full header

            # TODO send message to SQS with byte ranges
        if (window_start + int(5e9)) >= obj_size:
            window_end = obj_size

            # TODO send message to SQS with byte ranges

