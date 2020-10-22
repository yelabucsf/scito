import boto3
import functools
import numpy as np
from scito_count.BlockSplit import *

'''
Class to parse BGZF file and split into multiple chunks and copy those chunks as byte ranges from one s3 object to multiple
'''


class FileSplit(object):
    __slots__ = "ranges", "block_split", "n_parts"

    def __init__(self, block_split: BlockSplit, n_parts: int):
        self.block_split = block_split
        self.n_parts = n_parts
        self.ranges = None

    @classmethod
    def create_ranges(cls, func_of_technology):
        @functools.wraps(func_of_technology)
        def create_range_wrapper(self, *args, **kwargs):
            ranges = list(self.block_split)
            ranges = func_of_technology(self, ranges, *args, **kwargs)
            while len(ranges) < self.n_parts:
                arr_temp = np.array([func_of_technology(self, x, *args, **kwargs) for x in ranges])
                ranges = arr_temp.flatten()
            self.ranges = ranges
        return create_range_wrapper

class FQAdtAtacSplit(FileSplit):
    @FileSplit.create_ranges
    def adt_atac_ranges(self, ranges, overlap):
        ranges = np.array_split(ranges, 2)
        first_half = np.append(ranges[0], ranges[1][:overlap])
        second_half = np.append(ranges[0][-overlap:], ranges[1])
        return np.array([first_half, second_half])
