import functools
import operator
import numpy as np
from scito_count.BlockSplit import *

'''
Class to create a catalog of byte ranges to split files, based on all detected BGZF blocks from BlockSplit
'''


class BlockCatalog(object):
    __slots__ = "ranges", "block_split", "n_parts"

    def __init__(self, block_split, n_parts: int):
        '''
        :param block_split: BlockSplit type
        :param n_parts: Number of parts to split the file to
        '''
        self.block_split = block_split
        self.n_parts = n_parts
        self.ranges = None

    @classmethod
    def create_catalog(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def create_range_wrapper(self, *args, **kwargs):
            ranges = list(self.block_split)
            ranges = func_of_technology(self, ranges, *args, **kwargs)
            while len(ranges) < self.n_parts:
                arr_temp = [func_of_technology(self, x, *args, **kwargs) for x in ranges]
                ranges = functools.reduce(operator.iconcat, arr_temp, [])
            self.ranges = [(x[0][0], x[-1][-1]) for x in ranges]
        return create_range_wrapper



class FQAdtAtacCatalog(BlockCatalog):
    @BlockCatalog.create_catalog
    def adt_atac_catalog(self, ranges, overlap):
        ranges = np.array_split(ranges, 2)
        if overlap == 0:
            first_half = np.array(ranges[0])
            second_half = np.array(ranges[1])
        else:
            first_half = np.concatenate((ranges[0], ranges[1][:overlap]))
            second_half = np.concatenate((ranges[0][-overlap:], ranges[1]))
        return [first_half, second_half]
