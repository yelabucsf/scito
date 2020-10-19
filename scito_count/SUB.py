from scito_count.SeqFile import *
from typing import Tuple
'''
Class of aligned data format Seq - UMI - Barcode (SUB)
'''

class SUB(object):
    __slots__ = "sequence", "umi", "barcode", "flag"
    def __init__(self):
        pass


    def align(self, reads):
        '''
        alignment method
        :param reads: Tuple[SeqFile, SeqFile...]. Tuple of relevant seq files (combinations of R1, R2 and R3)
        :return: Void. Writes SUB file directly to S3
        '''

        
