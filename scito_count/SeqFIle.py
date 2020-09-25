import os
import boto3
import re
import gzip


from scito_count.ReadRecord import ReadRecord
from scito_count.S3Interface import S3Interface
from typing import Dict, Generator, List, Optional, Tuple

class SeqFile(object):
    __slots__ = "read_records", "s3_bucket", "s3_object_key", "technology", "read_type", "n_reads"
    def __init__(self, s3_bucket, s3_object_key):
        self.s3_bucket: str = s3_bucket
        self.s3_object_key = s3_object_key
        if self.s3_object_key.split(".")[-1] != "gz":
            raise ValueError("SeqFile(): object is not a gzip file")
        self.technology: str = None
        self.read_type: str = None
        self.n_reads: str = None

    def importRecord(self, func):
        s3_interface: S3Interface = S3Interface(self.s3_bucket, self.s3_object_key)
        def textParser(*args, **kwargs):
            with gzip.GzipFile(fileobj=s3_interface.full_name.get()["Body"]) as gzipfile:
                content = gzipfile.read()

        return textParser





class FastqFile(SeqFile):
    def __init__(self, s3_object, qc_scale="phred"):
        super().__init__(s3_object)
        self.qc_scale = qc_scale
        if qc_scale not in ["phred", "solexa"]:
            raise ValueError("FastqFile(): Illegal quality scale")







'''
getsizeof()
'''





