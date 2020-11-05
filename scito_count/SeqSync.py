from scito_count.SeqFile import *
import functools

class SeqSync(object):
    '''
    Class to synchronize multiple files to start from the same FQ id
    :param seq_files:   Dict[str: SeqFile]. Dictionary of seq files with keys read1, read2 ... readN
    :param ground_truth: str. Key of seq_files which is considered to be the ground truth: usually file created by
                        BlockCatalog without overlaps (overlap=0). Other SeqFile in the dict will have parts of the
                        earlier blocks and run into next blocks
    :return:            SeqSync object with SeqSync.self.seq_files = synced dictionary + other attrs
    '''
    def __init__(self, seq_files, ground_truth):
        self.seq_files = seq_files
        self.ground_truth = ground_truth
        if ground_truth not in seq_files.keys():
            raise KeyError("SeqSync(): dictionary key for ground_truth is not found in provided seq_files dictionary."
                           "Current dictionary contains {seq_files.keys()}")
        ground_truth_record = next(self.seq_files[ground_truth].read_records)
        self.ground_truth_id = ground_truth_record.read_id.split(" ")[0]

class FQSync(SeqSync):
    @classmethod
    def sync(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def sync_wrapper(self, *args, **kwargs):
            func_of_technology(self, *args, **kwargs)
            return self.seq_files
        return sync_wrapper


class FQSyncTwoReads(FQSync):
    '''
    This class for tech with 2 reads only.
    '''
    # TODO For now it looses the first synced read which is no big deal. Refactor to keep it???
    @FQSync.sync
    def two_read_sync(self):
        counter = 0
        key_out_of_sync = [x for x in self.seq_files.keys() if x != self.ground_truth]
        if len(key_out_of_sync) != 1:
            raise KeyError("FQSyncAdtAtac.adt_atac_sync(): this technology expects read2 and read3. More reads were provided")
        target_sync_record = next(self.seq_files[key_out_of_sync[0]].read_records)
        target_sync_record_id = target_sync_record.read_id.split(" ")[0]
        while target_sync_record_id != self.ground_truth_id:
            target_sync_record = next(self.seq_files[key_out_of_sync[0]].read_records)
            target_sync_record_id = target_sync_record.read_id.split(" ")[0]
            counter += 1
            if counter > 1000:
                raise ValueError("FQSyncTwoReads.two_read_sync(): Could not synchronize reads after 1000 attempts."
                                 "Make sure supplied reads are synchronizable at all.") # TODO catch this exception for to change ground truth read


