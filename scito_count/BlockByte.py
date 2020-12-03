import struct


class BlockByte(object):
    def __init__(self, block_split):
        '''
        :param block_split: BlockSplit type
        '''
        self.block_generator = block_split.generate_blocks()

    def byte_blocks(self):
        self.byte_block_gen = self._byte_blocks_inner()

    def _byte_blocks_inner(self):
        for block_start, block_end in self.block_generator:
            byte_string = struct.pack('<QQ', block_start, block_end)
            yield byte_string