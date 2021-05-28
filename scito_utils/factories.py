from typing import Type

from scito_count.BitFile import BitFile, BUSFileAdtAtac
from scito_count.SeqFile import SeqFile,FQFile
from scito_count.BitHeader import BUSHeaderAdtAtac
from scito_count.SeqSync import SeqSync, FQSyncTwoReads
from scito_count.SeqArranger import SeqArranger, FQSeqArrangerAdtAtac

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

def bit_header_factory(technology: str) -> bytes:
    technologies = {
        'scito ATAC': BUSHeaderAdtAtac
    }
    header_init = technologies[technology]()
    header = header_init.output_header()
    return header

def seq_sync_factory(technology: str) -> Type[SeqSync]:
    technologies = {
        'scito ATAC': FQSyncTwoReads
    }
    return technologies[technology]

def seq_arranger_factory(technology: str) -> Type[SeqArranger]:
    technologies = {
        'scito ATAC': FQSeqArrangerAdtAtac
    }
    return technologies[technology]
