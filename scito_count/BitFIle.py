from scito_count.BitHeader import *
from scito_count.BitRecord import *
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *

class BitFile(object):
    __slots__ = 'header', 'bit_records'

    def __init__(self):
        '''
        Main class for assembly and output of Bit file (BUS and possibly other formats)
        '''
