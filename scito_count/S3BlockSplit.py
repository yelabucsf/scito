import struct
from scito_count.S3Interface import S3Interface
from scito_count.ProcessSettings import *

'''
Deprecated
Class calculates offset ON S3 for each BGZF block and output a generator with block boundaries (start, end)
'''


class S3BlockSplit(object):
    def __init__(self, s3_settings: S3Settings):
        self.s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
        self.curr_offset: int = 0

    def _get_bgzf_block_size(self):
        '''
        Method to scan each BGZF header to get size of the block
        :return: int. Block size
        '''
        self.handle = self.s3_interface.get_bytes_s3(self.curr_offset, self.curr_offset + 32)
        magic = self.handle.read(4)    # MAGIC 4 bytes of a single block gzip ID
        if not magic:
            raise StopIteration
        _bgzf_magic = b"\x1f\x8b\x08\x04"
        if magic != _bgzf_magic:  # BGZF ID1, ID2, CM (compression method), flags
            raise ValueError(
                r"A BGZF block should start with "
                r"%r, not %r; handle.tell() now says %r"
                % (_bgzf_magic, magic, self.curr_offset)
            )
        self.handle.read(6)
        extra_len = struct.unpack("<H", self.handle.read(2))[0]

        block_size = None
        x_len = 0
        while x_len < extra_len:
            subfield_id = self.handle.read(2)
            subfield_len = struct.unpack("<H", self.handle.read(2))[0]  # uint16_t
            subfield_data = self.handle.read(subfield_len)
            x_len += subfield_len + 4
            if subfield_id == b"BC":    # magic number for
                if subfield_len != 2:
                    raise ValueError("BlockSplit._get_bgzf_block_size(): Wrong BC payload length")
                if block_size is not None:
                    raise ValueError("BlockSplit._get_bgzf_block_size(): Multiple BC fields")
                block_size = struct.unpack("<H", subfield_data)[0] + 1  # uint16_t
        assert x_len == extra_len, (x_len, extra_len)
        if block_size is None:
            raise ValueError("BlockSplit._get_bgzf_block_size(): Missing BC, this isn't a BGZF file!")

        self.curr_offset += block_size
        return block_size

    def generate_blocks(self):
        while True:
            try:
                block_size = self._get_bgzf_block_size()
            except StopIteration:
                break
            yield self.curr_offset - block_size, self.curr_offset - 1

