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

    def create_catalog(self, content_table, overlap):
        '''
        :param content_table: ContentTable type
        '''
        ranges = self._half_split(content_table, overlap)
        while len(ranges) < self.n_parts:
            arr_temp = [self._half_split(x, overlap) for x in ranges]
            ranges = functools.reduce(operator.iconcat, arr_temp, [])
        self.ranges = np.array([(x[0][0], x[-1][-1]) for x in ranges])

    def _half_split(self, content_table, overlap):
            content_table = np.array_split(content_table, 2)
            if overlap == 0:
                first_half = np.array(content_table[0])
                second_half = np.array(content_table[1])
            else:
                first_half = np.concatenate((content_table[0], content_table[1][:overlap]))
                second_half = np.concatenate((content_table[0][-overlap:], content_table[1]))
            return [first_half, second_half]
