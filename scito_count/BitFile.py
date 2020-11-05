from scito_count.BitHeader import *
from scito_count.BitRecord import *
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *
from scito_count.SeqSync import *
import functools

class BitFile(object):
    __slots__ = 'seq_sync', 'bit_records'

    def __init__(self, seq_sync: SeqSync):
        '''
        Main class for assembly and output of Bit file (BUS and possibly other formats). Input - generators with ReadRecord
        :param seq_sync: SeqSync. SeqSync object
        '''
        self.seq_sync = seq_sync

class BUSFile(BitFile):
    @classmethod
    def bus_file_stream(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def bus_file_stream_wrapper(self, *args, **kwargs):
            if not self.seq_sync.is_synched:
                raise AttributeError("BUSFileAdtAtac.bus_file_stream_adt_atac(): reads are not in sync")
            self.bit_records = func_of_technology(self, *args, **kwargs)
        return bus_file_stream_wrapper


class BUSFileAdtAtac(BUSFile):
    @BUSFile.bus_file_stream
    def bus_file_stream_adt_atac(self):
        bus_container = BUSRecordAdtAtac()
        for read2, read3 in zip(self.seq_sync.seq_files['read2'].read_records,
                                self.seq_sync.seq_files['read3'].read_records):
            bus_record = bus_container.construct_record((read2, read3))
            yield bus_record