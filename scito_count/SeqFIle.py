import os
import boto3
import re
import gzip
import functools

from scito_count.ReadRecord import FQRecord
from scito_count.S3Interface import S3Interface
from typing import Dict, Generator, List, Optional, Tuple

class SeqFile(object):
    __slots__ = "read_records", "s3_bucket", "s3_object_key", "technology", "read_type", "n_reads"
    def __init__(self, s3_bucket, s3_object_key):
        self.s3_bucket: str = s3_bucket
        self.s3_object_key = s3_object_key
        if self.s3_object_key.split(".")[-1] not in ["gz", "gzip"]:
            raise ValueError("SeqFile(): object is not a gzip file")
        self.technology: str = None
        self.read_type: str = None
        self.n_reads: str = None
        self.read_records: FQRecord = None

    @classmethod
    def import_record(cls, func):
        @functools.wraps(func)
        def text_parser(self, *args, **kwargs):
            s3_interface: S3Interface = S3Interface(self.s3_bucket, self.s3_object_key)
            with gzip.GzipFile(fileobj=s3_interface.full_name.get()["Body"], mode="r") as gzipfile:
                for line in gzipfile:
                    func(self, line, *args, **kwargs)
        return text_parser


def get_groups(seq, group_by):
    data = []
    for line in seq:
        # Here the `startswith()` logic can be replaced with other
        # condition(s) depending on the requirement.
        if line.startswith(group_by):
            if data:
                yield data
                data = []
        data.append(line)

    if data:
        yield data






class FastqFile(SeqFile):
    def __init__(self, s3_object, qc_scale="phred"):
        super().__init__(s3_object)
        self.qc_scale = qc_scale
        if qc_scale not in ["phred", "solexa"]:
            raise ValueError("FastqFile(): Illegal quality scale")

    @SeqFile.import_record
    def import_record_fastq(self, line):
        '''
        :return: read_block
        '''
        count = 0



    def read_record_block(self, ):
        self.read_records: List[FQRecord] = [import_record_fastq(x) for x in SOME_ITERATOR]





with open('input.txt') as f:
    for i, group in enumerate(get_groups(f, ">"), start=1):
        print ("Group #{}".format(i))
        print ("".join(group))




'''
getsizeof()
'''


def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        func(*args, **kwargs)


        print("Something is happening after the function is called.")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def someFunc(x):
    return x




samp = "/Users/antonogorodnikov/Documents/Work/Python/scito/tests/count_test/mock_data/TESTX_H7YRLADXX_S1_L001_R1_001.fastq.gz"

def get_groups(seq, n_lines):
    data = []
    counter = 0
    for line in seq:
        # Here the `startswith()` logic can be replaced with other
        # condition(s) depending on the requirement.
        if counter >= n_lines:
            yield data
            data = []
        data.append(line.strip())
        counter += 1
    if data:
        yield data

with gzip.GzipFile(samp, mode="r") as gzipfile:
    for line in gzipfile:
        get_groups(line.decode('utf-8'), 4)