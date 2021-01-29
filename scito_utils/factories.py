from typing import Type

from scito_count.BitFile import *
from scito_count.SeqFile import *


def seq_file_factory(technology: str) -> Type[SeqFile]:
    technologies = {
        'scito ATAC': FQFile
    }
    return technologies[technology]

def bit_file_factory(technology: str) -> Type[BitFile]:
    technologies = {
        'scito ATAC': BUSFileAdtAtac
    }
    return technologies[technology]

def bit_header_factory(technology: str) -> Type[BitHeader]:
    technologies = {
        'scito ATAC': BUSHeaderAdtAtac
    }
    header_init = technologies[technology]()
    header = header_init.output_header()
    return header




def seq_sync_factory(technology: Tuple) -> Type[SeqSync]:
    pass