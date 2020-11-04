from scito_count.ReadArranger import *

for read2, read3 in zip(self.reads[0].read_records, self.reads[1].read_records):
    if read2.read_id.split(" ")[0] != read3.read_id.split(" ")[0]:
        raise ValueError("FQAdtAtacArranger(): supplied reads in different order. Aborting!")
    read2_block = [read2.read_id, read2.seq + read3.seq[5:10], "+", # magic number
                   read2.quality_score + read3.quality_score[5:10]] # magic number
    fixed_read2 = FQAdtAtac(read_block=read2_block, read_start=0, read_end=len(read2_block[1]))
    yield fixed_read2
