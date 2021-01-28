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




def seq_sync_factory(technology: Tuple) -> Type[SeqSync]:
    technologies