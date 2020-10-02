import gzip

from scito_count.ReadRecord import *
from scito_count.S3Interface import S3Interface
from typing import List

class SeqFile(object):
    __slots__ = "read_records", "s3_bucket", "s3_object_key", "technology", "read_type", "n_reads"
    def __init__(self, s3_bucket, s3_object_key, config_file):
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
                with gzip.GzipFile(fileobj=s3_interface.s3_obj.get()["Body"], mode="r") as gzipfile:
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
    def import_record_fastq(self, data) -> None:
        self.read_records: List[FQRecord] = list(FQAdtAtac.parse_adt_atac(read_block=data, read_start="TODO", read_end="TODO")) # TODO: map specific read/tech to the subclass






'''
TODO 
Read types somewhere

allowed_read_types = ["R1", "R2", "R3"]
if read_type not in allowed_read_types:
    raise ValueError("FQRecord(): unknown read type. Must be R1, R2 or R3")

'''

