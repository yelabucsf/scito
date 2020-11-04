from scito_count.BitHeader import *
from scito_count.BitRecord import *
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *
from typing import Dict

class BitFile(object):
    __slots__ = 'header', 'bit_records'

    def __init__(self, seq_files: Dict[str: ""]):
        '''
        Main class for assembly and output of Bit file (BUS and possibly other formats)
        '''
