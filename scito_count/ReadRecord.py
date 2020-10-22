import re
from typing import List, Tuple
import functools


class ReadRecord(object):
    __slots__ = "read_id", "seq"

    def __init__(self):
        pass

    @classmethod
    def read_block_to_text(cls, func_of_read_type):
        @functools.wraps(func_of_read_type)
        def read_block_to_text_wrapper(self, *args, **kwargs):
            export_block: str = "\n".join(func_of_read_type(self, *args, **kwargs))+"\n"
            return export_block
        return read_block_to_text_wrapper


class FQRecord(ReadRecord):
    __slots__ = "quality_score"

    @classmethod
    def parse_read_block(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def parse_read_block_wrapper(self, read_block, *args, **kwargs):
            self.read_id: str = read_block[0]
            func_of_technology(self, read_block, *args, **kwargs)
            if not self.read_id.startswith("@"):
                raise ValueError("FQRecord(): passed read is NOT in FASTQ format")
            if not re.match('^[ATGCN]+$', self.seq):
                raise ValueError("FQRecord(): passed read is NOT a DNA sequence")
        return parse_read_block_wrapper

    @ReadRecord.read_block_to_text
    def fq_block_to_text(self):
        block: List[str] = [self.read_id, self.seq, "+", self.quality_score]
        return block



class FQAdtAtac(FQRecord):
    @FQRecord.parse_read_block
    def __init__(self, read_block: List[str], read_start: int, read_end: int):

        '''
        :param read_start: Int. Start position of the read. Depends on the technology
        :param read_end: Int. End position of the read. Depends on the technology
        '''
        seq = read_block[1][read_start: read_end]
        quality_score = read_block[3][read_start: read_end]
        if len(seq) < read_end:
            raise ValueError("FQAdtAtacSplit(): encountered read is truncated. Aborting")
        self.seq = seq
        self.quality_score = quality_score
