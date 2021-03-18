from scito_count.ReadArranger import *
from scito_count.SeqSync import *

class SeqArranger(object):
    '''
    Generator class of arranged read records (stitched sequences)
    :param seq_sync: SeqSync. Synced generators of multiple reads to be arranged
    :returns: generator of ReadRecords
    '''
    __slots__ = 'seq_sync', 'read_records'
    def __init__(self, seq_sync: SeqSync):
        self.seq_sync = seq_sync

class FQSeqArrangerAdtAtac(SeqArranger):
    def __init__(self, seq_sync):
        super().__init__(seq_sync)
        self.read_records = self.arrange_sequences()

    def arrange_sequences(self):

        read_file2 = self.seq_sync.seq_files[0]
        read_file3 = self.seq_sync.seq_files[1]

        for read2, read3 in zip(read_file2.read_records, read_file3.read_records):
            if read2.read_id.split(" ")[0] != read3.read_id.split(" ")[0]:
                raise ValueError("FQSeqArrangerAdtAtac.arrange_sequences(): supplied reads in different order. Aborting!")
            read2_block = [read2.read_id, read2.seq + read3.seq[5:10], "+", # magic number: array range
                           read2.quality_score + read3.quality_score[5:10]] # magic number: array range
            fixed_read2 = FQRecordAdtAtac(read_block=read2_block, read_start=0, read_end=len(read2_block[1]))
            yield fixed_read2
