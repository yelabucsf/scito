from scito_count.ReadArranger import *
from scito_count.SeqSync import *

class SeqArranger(object):
    '''
    Generator class of arranged read records (stitched sequences)
    :param seq_sync: SeqSync. Synced generators of multiple reads to be arranged
    :returns: generator of ReadRecords
    '''
    __slots__ = "seq_sync"
    def __init__(self, seq_sync: SeqSync):
        self.seq_sync = seq_sync

class FQSeqArrangerAdtAtac(SeqArranger):
    def arrange_sequences(self):
        # checking consistency of seq_files dictionary
        supplied_names = self.seq_sync.seq_files.keys()
        if not all(names in supplied_names for names in ['read2', 'read3']):
            raise KeyError("FQSeqArrangerAdtAtac.arrange_sequences(): For seq_files expect dictionary with keys 'read2',"
                           f"'read3'. Provided dictionary with keys: {self.seq_sync.seq_files.keys()}. Aborting!")
        read_file2 = self.seq_sync.seq_files['read2']
        read_file3 = self.seq_sync.seq_files['read3']

        for read2, read3 in zip(read_file2.read_records, read_file3.read_records):
            if read2.read_id.split(" ")[0] != read3.read_id.split(" ")[0]:
                raise ValueError("FQSeqArrangerAdtAtac.arrange_sequences(): supplied reads in different order. Aborting!")
            read2_block = [read2.read_id, read2.seq + read3.seq[5:10], "+", # magic number: array range
                           read2.quality_score + read3.quality_score[5:10]] # magic number: array range
            fixed_read2 = FQRecordAdtAtac(read_block=read2_block, read_start=0, read_end=len(read2_block[1]))
            yield fixed_read2