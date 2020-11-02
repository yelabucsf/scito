from typing import List, Tuple
import functools
from scito_count.ReadRecord import *


class BitRecord(object):
    def __init__(self):
        pass

    def get_seq_fragment(self, read_record, start: int=0 , seq_length: int=0):
        '''
        extracts read string
        :param read_record: ReadRecord
        '''
        seq = read_record.seq
        if seq_length == 0:
            seq_length = len(seq)
        return seq[start: start + seq_length]

    def bit_seq(self):
        pass
        # TODO implement in case decide to skip BUS Tools


class BUSRecord(BitRecord):
    __slots__ = "bc", "umi", "seq"
    @classmethod
    def construct_bus(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def construct_bus_wrapper(self, *args, **kwargs):
            func_of_technology(self, *args, **kwargs)
        return construct_bus_wrapper


class AdtAtacBus(BUSRecord):
    @BUSRecord.construct_bus
    def construct_record(self, reads):
        '''
        :param reads: Tuple[ReadRecord, ReadRecord]. Tuple of read records corresponding to the technology description.
        reads[0] = read 2
        reads[1] = read 3
        Reads are already arranged and trimmed
        '''
        # TODO refactor this piece

        self.bc = self.get_seq_fragment(reads[0],0 ,0)
        self.umi = self.get_seq_fragment(reads[1], 10, 18)
        self.seq = self.get_seq_fragment(reads[1], 0, 5)
        return self










