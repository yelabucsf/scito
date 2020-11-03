from scito_count.SeqFile import *
from scito_count.ReadRecord import *

'''
Class primarily for kallisto BUS test. Will be obsolete fi binary search works faster
'''

class ReadArranger(object):
    __slots__ = "seq_files"

    def __init__(self, seq_files):
        '''
        :param seq_files: Tuple[SeqFile]. Contains tuple of SeqFiles in the order R1, R2, R3 if applicable
        '''
        self.reads: Tuple[SeqFile] = seq_files


class FQAdtAtacArranger(ReadArranger):
    '''
    Class contains only read2 and read3 - per technology description. So FQAdtAtacArranger.reads[0] is "read2"
    and FQAdtAtacArranger.reads[1] is "read3"
    :return generator.FQAdtAtacSplit. read2 (Cell barcode 16nt) + 5nt of well barcode
    '''
    def arrange(self):
        for read2, read3 in zip(self.reads[0].read_records, self.reads[1].read_records):
            if read2.read_id.split(" ")[0] != read3.read_id.split(" ")[0]:
                raise ValueError("FQAdtAtacArranger(): supplied reads in different order. Aborting!")
            read2_block = [read2.read_id, read2.seq + read3.seq[5:10], "+", # magic number
                           read2.quality_score + read3.quality_score[5:10]] # magic number
            fixed_read2 = FQAdtAtac(read_block=read2_block, read_start=0, read_end=len(read2_block[1]))
            yield fixed_read2





