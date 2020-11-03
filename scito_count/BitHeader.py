import struct
import functools

class BitHeader(object):
    def __init__(self):
        pass


class BUSHeader(BitHeader):
    def __init__(self):
        super().__init__()
        self.magic = b'BUS\0'
        self.version = b'gvai'  # proprietary version for sito-seq

    @classmethod
    def output_header(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def output_header_wrapper(self, *args, **kwargs):
            header = b''.join([self.magic,
                               self.version,
                               func_of_technology(self, *args, **kwargs)])
            return header
        return output_header_wrapper

class AdtAtacBusHeader(BUSHeader):
    def __init__(self):
        super().__init__()
        self.bc_len = struct.pack('<L', 21)
        self.umi_len = struct.pack('<L', 8)
        self.text = b'scito-seq ADT 10x ATAC v1'
        self.tlen = struct.pack('<L', len(self.text))

    @BUSHeader.output_header
    def output_adt_atac_header(self):
        return b''.join([self.bc_len, self.umi_len, self.tlen, self.text])

