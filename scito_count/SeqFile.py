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
    def import_record(cls, n_lines):
        def import_record_inner(func):
            @functools.wraps(func)
            def text_parser(self, *args, **kwargs):
                s3_interface: S3Interface = S3Interface(self.s3_bucket, self.s3_object_key)
                with gzip.GzipFile(fileobj=s3_interface.full_name.get()["Body"], mode="r") as gzipfile:
                    data: List[str] = []
                    counter = 0
                    for line in gzipfile:
                        line_decoded = line.decode('utf-8')
                        if counter >= n_lines:
                            yield func(data, *args, **kwargs)
                            data = []
                            counter = 0
                        data.append(line_decoded.strip())
                        counter += 1
                    if data:
                        yield func(data, *args, **kwargs)
            return text_parser
        return import_record_inner


class FastqFile(SeqFile):
    def __init__(self, qc_scale="phred"):
        super().__init__(qc_scale)
        self.qc_scale = qc_scale
        if qc_scale not in ["phred", "solexa"]:
            raise ValueError("FastqFile(): Illegal quality scale")

    @SeqFile.import_record(4)   # FASTQ file - 4 lines per block
    def import_record_fastq(self, data):
        self.read_records: List[FQRecord] = list(FQRecord(data))







'''
getsizeof()
'''


samp = "/Users/antonogorodnikov/Documents/Work/Python/scito/tests/count_test/mock_data/TESTX_H7YRLADXX_S1_L001_R1_001.fastq.gz"

def get_groups(seq, n_lines):
    data = []
    counter = 0
    for line in seq:
        line_decoded = line.decode('utf-8')
        # Here the `startswith()` logic can be replaced with other
        # condition(s) depending on the requirement.
        if counter >= n_lines:
            yield data
            data = []
            counter = 0
        data.append(line_decoded.strip())
        counter += 1
    if data:
        yield data

gen = list()
with gzip.GzipFile(samp, mode="r") as gzipfile:
    gen.extend(get_groups(gzipfile, 4))



def import_record(n_lines):
    def import_record_inner(func):
        @functools.wraps(func)
        def text_parser(*args, **kwargs):
            with gzip.GzipFile(samp, mode="r") as gzipfile:
                data: List[str] = []
                counter = 0
                for line in gzipfile:
                    line_decoded = line.decode('utf-8')
                    if counter >= n_lines:
                        yield func(data, *args, **kwargs)
                        data = []
                        counter = 0
                    data.append(line_decoded.strip())
                    counter += 1
                if data:
                    yield func(data, *args, **kwargs)
        return text_parser
    return import_record_inner

@import_record(4)   # FASTQ file - 4 lines per block
def import_record_fastq(data):
    gen = list()
    id: str = data[0]
    seq: str = data[1]
    quality_score = data[3]
    return [id, seq, quality_score]
    #return gen

kk = import_record_fastq()

