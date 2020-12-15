import functools
import operator
import numpy as np
from scito_count.BlockSplit import *

'''
Class to create a catalog of byte ranges to split files, based on all detected BGZF blocks from BlockSplit
'''


class BlockCatalog(object):
    __slots__ = "ranges", "block_split", "n_parts"

    def __init__(self, n_parts: int):
        '''
        :param n_parts: Number of parts to split the file to
        '''
        self.n_parts = n_parts
        self.ranges = None

    @classmethod
    def create_catalog(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def create_range_wrapper(self, content_table, *args, **kwargs):
            '''
            :param content_table: ContentTable type
            '''
            ranges = func_of_technology(self, content_table, *args, **kwargs)
            while len(ranges) < self.n_parts:
                arr_temp = [func_of_technology(self, x, *args, **kwargs) for x in ranges]
                ranges = functools.reduce(operator.iconcat, arr_temp, [])
            self.ranges = [(x[0][0], x[-1][-1]) for x in ranges]
        return create_range_wrapper



class FQAdtAtacCatalog(BlockCatalog):
    @BlockCatalog.create_catalog
    def adt_atac_catalog(self, content_table, overlap):
        content_table = np.array_split(content_table, 2)
        if overlap == 0:
            first_half = np.array(content_table[0])
            second_half = np.array(content_table[1])
        else:
            first_half = np.concatenate((content_table[0], content_table[1][:overlap]))
            second_half = np.concatenate((content_table[0][-overlap:], content_table[1]))
        return [first_half, second_half]
