import struct


class BlockByte(object):
    def __init__(self, block_split):
        '''
        Class to generate byte strings from offsets of BGZF ranges
        :param block_split: BlockSplit type
        '''

        if block_split.ranges is None:
            block_split.generate_blocks()

        self.block_generator = block_split

    def byte_blocks(self):
        self.byte_block_gen = self._byte_blocks_inner()

    def _byte_blocks_inner(self):
        for block_start, block_end in self.block_generator.ranges:
            byte_string = struct.pack('<QQ', block_start, block_end)
            yield byte_string
