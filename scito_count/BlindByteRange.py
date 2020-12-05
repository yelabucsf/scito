import subprocess as sp
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *

'''
Class generates a blind catalog of large files producing a range of 1 Gb + 18 bytes (to avoid BGZF header split)
This is done because files > 12 Gb take over 1 min to get proper BlockCatalog, which is not suitable for lambda.
Target - get files down to 5 Gb.
'''
class BlindByteRange(object):
    def __init__(self, s3_settings: S3Settings):
        s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
        self.obj_size = s3_interface.obj_size()
        self.window_size = int(1e9) # KEEP CONSTANT - 1 Gb chunk sizes
        self.overlap = 18   # 18 bytes is the BGZF full header

    def generate_blind_ranges(self):
        window_start = 0
        while (window_start + self.window_size + self.overlap) < self.obj_size:
            window_end = window_start + self.window_size
            start_end = window_start, window_end
            yield start_end
            window_start += window_end - self.overlap

        if (window_start + self.window_size) >= self.obj_size:
            yield window_start, self.obj_size





