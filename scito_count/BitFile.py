from scito_count.BitRecord import *
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

    @classmethod
    def bit_file_stream(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def bit_file_stream_wrapper(self, *args, **kwargs):
            if not self.seq_sync.is_synced:
                raise AttributeError("BUSFileAdtAtac.bus_file_stream_adt_atac(): reads are not in sync")
            self.bit_records = func_of_technology(self, *args, **kwargs)

        return bit_file_stream_wrapper


class BUSFileAdtAtac(BitFile):
    @BitFile.bit_file_stream
    def bus_file_stream(self):
        bus_container = BUSRecordAdtAtac()
        for read2, read3 in zip(self.seq_sync.seq_files[0].read_records,
                                self.seq_sync.seq_files[1].read_records):
            bus_record = bus_container.construct_record((read2, read3))
            yield bus_record
