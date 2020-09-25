import re
from typing import List


class ReadRecord(object):
    __slots__ = "id", "seq"


class FQRecord(ReadRecord):
    __slots__ = "quality_score"
    def __init__(self, read_block: List[str]):
        self.id: str = read_block[0]
        self.seq: str = read_block[1]
        self.quality_score: str = read_block[3]
        if not self.id.startswith("@"):
            raise ValueError("FQRecord(): passed read is NOT in FASTQ format")
        if not re.match('^[ATGCN]+$', self.seq):
            raise ValueError("FQRecord(): passed read is NOT a DNA sequence")




