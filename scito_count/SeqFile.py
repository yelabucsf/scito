import gzip
from scito_count.ReadRecord import *
from scito_count.S3Interface import S3Interface
from scito_count.ProcessSettings import *
from typing import List


class SeqFile(object):
    '''
    Class containing all sequencing records of a file + meta data
    :param s3_settings: S3Settings. Configuration for an S3 access. See ProcessSettings.py
    :param read_settings: ReadSettings. Configuration for the read format. See ProcessSettings.py
    :param byte_range: str. Format 'start-end'. Byte offsets to download from S3
    :return SeqFile object
    '''

    __slots__ = "read_records", "s3_interface", "technology", "n_reads", "byte_range"

    def __init__(self, s3_settings: S3Settings, read_settings: ReadSettings, byte_range: str, **kwargs):
        self.s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, **kwargs)
        if s3_settings.object_key.split(".")[-1] not in ["gz", "gzip"]:
            raise ValueError("SeqFile(): object is not a gzip file")
        self.technology: ReadSettings = read_settings
        self.n_reads: str = None
        self.read_records: FQRecord = None
        self.byte_range: str = byte_range

    '''
    Classmethod to accept a method from subclass and process a set of lanes in input files
    :param n_lines: int. Number of lanes in a block. E.g. fastq file has a 4-lane block
    :return: Void. But writes a generator in self.read_records with ReadRecords as individual element. See ReadRecord.py
    '''

    @classmethod
    def import_record(cls, n_lines):
        def import_record_inner(func):
            @functools.wraps(func)
            def text_parser(self, *args, **kwargs):
                with gzip.GzipFile(fileobj=self.s3_interface.s3_obj.get(Range=f"bytes={self.byte_range}")["Body"],
                                   mode="r") as gzipfile:
                    data: List[str] = []
                    counter = 0
                    for line in gzipfile:
                        line_decoded = line.decode('utf-8')
                        if counter >= n_lines:
                            yield func(self, data, *args, **kwargs)
                            data = []
                            counter = 0
                        data.append(line_decoded.strip())
                        counter += 1
                    if data:
                        yield func(self, data, *args, **kwargs)

            return text_parser

        return import_record_inner


class FQFile(SeqFile):
    def __init__(self, s3_settings: S3Settings, read_settings: ReadSettings, byte_range: str, qc_scale="phred"):
        '''
        See parent class
        '''
        super().__init__(s3_settings, read_settings, byte_range)
        self.qc_scale = qc_scale
        if qc_scale not in ["phred", "solexa"]:
            raise ValueError("FastqFile(): Illegal quality scale")
        self.read_records = self.import_record_fastq()

    @SeqFile.import_record(4)  # FASTQ file - 4 lines per block
    def import_record_fastq(self, data):
        return FQRecordAdtAtac(read_block=data, read_start=int(self.technology.start),
                               read_end=int(self.technology.end))
