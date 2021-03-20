from scito_count.S3Interface import *
from scito_count.ProcessSettings import *

'''
Function generates a blind catalog of large files producing a range of 1 Gb + 18 bytes (to avoid BGZF header split)
This is done because files > 12 Gb take over 1 min to get proper BlockCatalog, which is not suitable for lambda.
Target - get blind chunks down to 1 Gb and load them into memory.
'''


def blind_byte_range(s3_settings: S3Settings):
    s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
    obj_size = s3_interface.obj_size()
    window_size = int(1e9)  # KEEP CONSTANT - 1 Gb chunk sizes
    overlap = 18  # 18 bytes is the BGZF full header

    window_start = 0
    while (window_start + window_size + overlap) < obj_size:
        window_end = window_start + window_size
        start_end = window_start, window_end
        yield start_end
        window_start += window_end - overlap

    if (window_start + window_size) >= obj_size:
        yield window_start, obj_size
