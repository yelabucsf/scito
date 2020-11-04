from scito_count.SeqFile import *
from scito_count.ReadRecord import *
from scito_count.SeqSync import *
from typing import Tuple

'''
Class to rearrange read records passed to it and output corrected read record. Use case scito ADT - move well bc to cell
bc read
'''

class ReadArranger(object):
    def __init__(self, read_records):
        '''
        :param seq_files: Tuple[ReadRecord]. Tuple of read records
        '''
        self.read_records = read_records


class FQArrangerAdtAtac(ReadArranger):
    '''
    Class contains only read2 and read3 - per technology description. self.read_records[0] is read2, self.read_records[1]
    is read3
    :return ReadRecord. rearranged read2 (Cell barcode 16nt) + 5nt of well barcode
    '''


    def arrange(self):
        read2, read3 = self.read_records
        if read2.read_id.split(" ")[0] != read3.read_id.split(" ")[0]:
            raise ValueError("FQArrangerAdtAtac(): supplied reads in different order. Aborting!")

        read2_block = [read2.read_id, read2.seq + read3.seq[5:10], "+", # magic number
                       read2.quality_score + read3.quality_score[5:10]] # magic number
        fixed_read2 = FQAdtAtac(read_block=read2_block, read_start=0, read_end=len(read2_block[1]))

        return fixed_read2





