from scito_count.SeqFile import *
import functools

class SeqSync(object):
    '''
    Class to synchronize multiple files to start from the same FQ id
    :param seq_files:   Dict[str: SeqFile]. Dictionary of seq files with keys read1, read2 ... readN
    :return:            SeqSync object with SeqSync.self.seq_files = synced dictionary + other attrs
    '''
    def __init__(self, seq_files: Tuple):
        self.seq_files = seq_files

        # Ground truth is a SeqFile object (first element of seq_files) which is considered to be the ground truth:
        # usually file created by BlockCatalog without overlaps (overlap=0). Other SeqFile in the dict will have parts
        # of the earlier blocks and run into next blocks
        self.ground_truth = seq_files[0]
        self.is_synched = False
        ground_truth_record = next(self.ground_truth.read_records)
        self.ground_truth_id = ground_truth_record.read_id.split(" ")[0]

class FQSync(SeqSync):
    @classmethod
    def sync(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def sync_wrapper(self, *args, **kwargs):
            func_of_technology(self, *args, **kwargs)
            self.is_synched = True  # Checkup for class calls
            return self.seq_files
        return sync_wrapper


class FQSyncTwoReads(FQSync):
    '''
    This class for tech with 2 reads only.
    '''
    # TODO For now it loses the first synced read which is no big deal. Refactor to keep it???
    @FQSync.sync
    def two_read_sync(self):
        counter = 0
        if len(self.seq_files) != 2:
            raise KeyError("FQSyncAdtAtac.adt_atac_sync(): this technology expects exactly 2 reads")
        target_sync_record = next(self.seq_files[1].read_records)
        target_sync_record_id = target_sync_record.read_id.split(" ")[0]
        while target_sync_record_id != self.ground_truth_id:
            target_sync_record = next(self.seq_files[1].read_records)
            target_sync_record_id = target_sync_record.read_id.split(" ")[0]
            counter += 1
            if counter > 1000:
                raise ValueError("FQSyncTwoReads.two_read_sync(): Could not synchronize reads after 1000 attempts."
                                 "Make sure supplied reads are synchronizable at all.") # TODO catch this exception for to change ground truth read


