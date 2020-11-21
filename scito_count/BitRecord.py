import functools
import struct
import numpy as np
from scito_count.ReadRecord import *
from numba import jit

class BitRecord(object):
    def __init__(self):
        pass

    def get_seq_fragment(self, read_record, start: int=0 , seq_length: int=0) -> str:
        '''
        extracts read string
        :param read_record: ReadRecord
        '''
        seq: str = read_record.seq
        if seq_length > len(read_record.seq):
            raise ValueError(f"BitRecord.get_seq_fragment(): sequence {read_record.read_id} is truncated. Aborting!")
        if seq_length == 0:
            seq_length = len(seq)
        return seq[start: start + seq_length]

    @staticmethod
    @jit
    def dna_to_twobit(dna: str) -> int:
        x: int = 0
        for nt in dna:
            if nt == "A":
                x += 0
            elif nt == "C":
                x += 1
            elif nt == "G":
                x += 2
            elif nt == "T":
                x += 3
            else:
                x += np.random.choice([0,1,2,3])
            x <<= 2
        x >>= 2
        return x

    # TODO implement smaller BUS (sBUS) when we want to skip bustools
    def sbus_encode(self):
        pass

class BUSRecord(BitRecord):
    @classmethod
    def construct_bus(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def construct_bus_wrapper(self, *args, **kwargs):
            int_bc, int_umi, int_seq = func_of_technology(self, *args, **kwargs)
            flag = 0 # TODO include some additional info like technology or smth
            byte_string = struct.pack('<QQLLLL', int_bc, int_umi, int_seq, 1, flag, 0)
            return byte_string
        return construct_bus_wrapper


class BUSRecordAdtAtac(BUSRecord):
    @BUSRecord.construct_bus
    def construct_record(self, reads):
        '''
        :param reads: Tuple[ReadRecord, ReadRecord]. Tuple of read records corresponding to the technology description.
        reads[0] = read 2
        reads[1] = read 3
        Reads are already arranged and trimmed
        '''
        # TODO refactor this piece
        bc = self.get_seq_fragment(reads[0], 0, 21)
        umi = self.get_seq_fragment(reads[1], 10, 18)
        seq = self.get_seq_fragment(reads[1], 0, 5)

        int_bc, int_umi, int_seq = [self.dna_to_twobit(x) for x in (bc, umi, seq)]
        return int_bc, int_umi, int_seq










