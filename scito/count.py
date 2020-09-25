import json
import numpy as np
from typing import List, Dict
import os
import pandas as pd
from scito.scitoSamples import ScitoSamples
from numba import jit
from tempfile import TemporaryDirectory
import logging
from scito.utils import execute
import scipy.sparse as sparse

# TODO create a ScitoSamples object from DF. Create DF first



def scito_count(ref: str, outdir: str, libraries: ScitoSamples,
                tmp: str, n_threads: int = 1, out_type: str = "h5ad") -> None:
    '''
    Function to execute alignment, count and filtering of FASTQ files using kallisto on the back end
    :param ref: str. Path to reference index created for kallisto
    :param outdir: str. Path to the out dir
    :param libraries: ScitoSamples with attributes:
        sample_id - Sample id
        technology - single cell techology used. Supported [3v3, ATAC]
        target_n_cell - expected number of cells (singlets)
        fastqs - ordered links to all FASTQ files
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
    kallisto_index = os.path.join(ref, manifest["index_file"])

    if tmp is None:
        tmp = os.path.join(outdir, "tmp")

    if not os.path.exists(tmp):
        os.mkdir(tmp)

    with TemporaryDirectory(dir=tmp) as temp:
        None
        # TODO stitch reads according to the tech

    with TemporaryDirectory(dir=tmp) as temp:
        cmd = ["kallisto", "bus", "-i", kallisto_index, "-o", temp, "-x",
               libraries.technology, "-t", str(n_threads)] + libraries.fastqs
        logging.info(" ".join(cmd))

        # from loompy
        for line in execute(cmd):
            if line != "\n":
                logging.info(line[:-1])




    # TODO barcode correction

path: str, os.path.join(d, "output.bus"),
genes_metadata_file: str, 			os.path.join(index_path, manifest["gene_metadata_file"]),
genes_metadata_key: str, 			manifest["gene_metadata_key"],
fragments2genes_file: str, 			os.path.join(index_path, manifest["fragments_to_genes_file"]),
equivalence_classes_file: str, 			os.path.join(d, "matrix.ec"),
fragments_file: str 			os.path.join(d, "transcripts.txt"


