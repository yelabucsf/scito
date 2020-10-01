import re
from typing import List, Tuple
import functools


class ReadRecord(object):
    __slots__ = "id", "seq"

    @classmethod
    def parse_read_block(cls, func_of_filetype):
        @functools.wraps(func_of_filetype)
        def block_parser(self, *args, **kwargs):
            parsed_features: Tuple[str] = func_of_filetype(*args, **kwargs)   # tuple of parsed features, specific to each subclass
            return parsed_features
        return block_parser


class FQRecord(ReadRecord):
    __slots__ = "quality_score"

    def __init__(self, read_type):
        allowed_read_types = ["R1", "R2", "R3"]
        if read_type not in allowed_read_types:
            raise ValueError("FQRecord(): unknown read type. Must be R1, R2 or R3")

    @ReadRecord.parse_read_block
    def parse_fq_read(self, read_block):
        self.read_id: str = read_block[0]
        self.seq: str = read_block[1]
        self.quality_score: str = read_block[3]
        if not self.read_id.startswith("@"):
            raise ValueError("FQRecord(): passed read is NOT in FASTQ format")
        if not re.match('^[ATGCN]+$', self.seq):
            raise ValueError("FQRecord(): passed read is NOT a DNA sequence")


class fq_adt_atac_r1(FQRecord):
    @FQRecord.parse_fq_read
    def __call__(self, read_block):
        self.seq = read_block[1][:16]
        self.quality_score = read_block[3][16]








