import json
import numpy as np
from typing import List
import os
import pandas as pd
from scito.scitoSamples import ScitoSamples


def scito_count(ref: str, outfile: str, libraries: ScitoSamples,
                tmp: str, n_threads: int = 1, out_type: str = "h5ad") -> None:
    '''
    Function to perform alignment, count and filtering of FASTQ files using kallisto on the back end
    :param ref: str. Path to reference index created for kallisto
    :param outfile: str. Path to the out dir
    :param libraries: ScitoSamples with attributes:
        sample_id - Sample id
        technology - single cell techology used. Supported [3v3, ATAC]
        target_n_cell - expected number of cells (singlets)
        R1 - link to FASTQ file with read 1
        R2 - link to FASTQ file with read 2
        R3 - link to FASTQ file with read 3 (optional if ATAC is used as technology)
    :param tmp: str. Path to the tmp directory
    :param n_threads: int. Number of threads for kallisto bus command
    :param out_type: str. Output data format. Accepts ('loom', 'h5ad') . Default = h5ad
    :return: Void. Creates a file in the output directory
    '''

    accepted_type = ['h5ad', 'loom']
    assert (out_type in accepted_type), "ValueError: scito.scito_count(). Unknown type of output file. " \
                                        "Accepted values: h5ad, loom"

    manifest_file = os.path.join(ref, "manifest.json")
    assert (os.path.exists(manifest_file)), "ValueError: scito.scito_count(). Manifest file is not in {}".format(ref)
    assert (libraries.sample_id is not None), "ValueError: scito.scito_count(). Libraries object is empty"

    with open(manifest_file) as f:
        manifest = json.load(f)

    kallisto_index = os.path.join(ref, )
    cmd = ["kallisto", "bus", "-i", kallisto_index,
           "-o", tmp, "-x", technology, "-t", str(n_threads)] + fastqs

    # TODO barcode correction
