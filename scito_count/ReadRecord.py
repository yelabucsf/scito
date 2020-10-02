import re
from typing import List, Tuple
import functools


class ReadRecord(object):
    __slots__ = "read_id", "seq"
    """@classmethod
    def parse_read_block(cls, func_of_filetype):
        @functools.wraps(func_of_filetype)
        def block_parser(self, *args, **kwargs):
            parsed_features: Tuple[str] = func_of_filetype(*args, **kwargs)   # tuple of parsed features, specific to each subclass
            return parsed_features
        return block_parser
"""


class FQRecord(ReadRecord):
    __slots__ = "quality_score"

    @classmethod
    def parse_read_block(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def parse_read_block_wrapper(self, read_block, *args, **kwargs):
            self.read_id: str = read_block[0]
            read_features: Tuple[str] = func_of_technology(read_block, *args, **kwargs)
            self.seq: str = read_features[0]
            self.quality_score: str = read_features[1]

            if not self.read_id.startswith("@"):
                raise ValueError("FQRecord(): passed read is NOT in FASTQ format")
            if not re.match('^[ATGCN]+$', self.seq):
                raise ValueError("FQRecord(): passed read is NOT a DNA sequence")

        return parse_read_block_wrapper


class FQAdtAtac(FQRecord):
    def __init__(self):
        pass
    @FQRecord.parse_read_block
    def parse_adt_atac(self, read_block, read_start, read_end):
        '''
        :param read_start: Int. Start position of the read. Depends on the technology
        :param read_end: Int. End position of the read. Depends on the technology
        '''
        seq = read_block[1][read_start: read_end]
        quality_score = read_block[3][read_start: read_end]
        if len(seq) < read_end:
            raise ValueError("FQAdtAtacR1.parse_adt_atac_r1: encountered read is truncated. Aborting")
        return seq, quality_score


