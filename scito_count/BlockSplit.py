from scito_count.BlockSearch import *
from scito_count.BlocksIO import *
from io import BytesIO
import struct

'''
Class to create a catalog of BGZF blocks in a single file.
Returns a generator of tuples of (block start, block end)
'''


class BlockSplit(object):
    __slots__ = "ranges", "handle", 'block_start', 'block_end',
    def __init__(self, handle):
        '''
        :param handle: BlocksIO
        '''
        self.handle = handle.data_stream
        self.block_start = handle.block_start
        self.block_end = handle.block_end
        self.ranges = None

    def generate_blocks(self):
        self.ranges = self._inner_generate_blocks()

    def _get_bgzf_block_size(self):
        '''
        Method to scan each BGZF header to get size of the block
        :return: int. Block size
        '''
        _bgzf_magic = b"\x1f\x8b\x08\x04"
        magic = self.handle.read(4)
        if not magic:
            raise StopIteration
        while magic != _bgzf_magic:
            raise ValueError(
                r"A BGZF (e.g. a BAM file) block should start with "
                r"%r, not %r; handle.tell() now says %r"
                % (_bgzf_magic, magic, self.handle.tell())
            )
        self.handle.seek(6 + self.handle.tell())
        extra_len = struct.unpack("<H", self.handle.read(2))[0]

        block_size = None
        x_len = 0
        while x_len < extra_len:
            subfield_id = self.handle.read(2)
            subfield_len = struct.unpack("<H", self.handle.read(2))[0]  # uint16_t
            subfield_data = self.handle.read(subfield_len)
            x_len += subfield_len + 4
            if subfield_id == b"BC":
                if subfield_len != 2:
                    raise ValueError("BlockSplit._get_bgzf_block_size(): Wrong BC payload length")
                if block_size is not None:
                    raise ValueError("BlockSplit._get_bgzf_block_size(): Multiple BC fields")
                block_size = struct.unpack("<H", subfield_data)[0] + 1  # uint16_t

        assert x_len == extra_len, (x_len, extra_len)
        if block_size is None:
            raise ValueError("BlockSplit._get_bgzf_block_size(): Missing BC, this isn't a BGZF file!")
        curr_pos = self.handle.tell()
        next_block = curr_pos - 18 + block_size # 18 bytes is the BGZF full header
        self.handle.seek(next_block)
        return block_size

    def _inner_generate_blocks(self):
        while True:
            start_offset = self.handle.tell()
            try:
                block_size = self._get_bgzf_block_size()
            except ValueError:
                self.handle.seek(0)
                block_search = BlockSearch(self.handle)
                real_header = block_search.header_search()
                self.handle.seek(real_header)
                start_offset = self.handle.tell()
                block_size = self._get_bgzf_block_size()
            except StopIteration:
                break
            yield start_offset + self.block_start,\
                  start_offset + self.block_start + block_size-1



