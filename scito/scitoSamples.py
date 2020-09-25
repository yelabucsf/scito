import numpy as np
from typing import List
import os
import re
import pandas as pd

class ScitoSamples():
    def __init__(self):
        '''
        Class containing sample meta data with the following attributes:
            sample_id : str - Sample id
            technology : str - single cell techology used. Supported [3v3, ATAC]
            target_n_cell : int - expected number of cells (singlets)
            R1 : List[str] - link to FASTQ file with read 1
            R2 : List[str] - link to FASTQ file with read 2
            R3 : List[str] - link to FASTQ file with read 3 (optional if ATAC is used as technology)
        '''

    def from_df(self, df):
        '''
        Fill in attributes with data from pandas.DataFrame
        :param df: pandas.DataFrame. Contains columns of the same name as class attributes.
        :return: Void. Populates class attributes
        '''
        uniques = [df[x].unique() for x in ["sample_id", "technology", "target_n_cell"]]
        assert (all(uniques) == 1), "ValueError: scito.ScitoSamples.from_df(). Meta file contains multiple samples " \
                                    "and/or technologies. "
        self.sample_id, self.technology, self.target_n_cell = [x[0] for x in uniques]

        self.R1, self.R2 = np.array([np.sort(np.array(df[x])) for x in ["R1", "R2"]])
        if self.technology == "scito":
            self.R3 = np.sort(np.array(df["R3"]))

        # test fastq presence
        regex = re.compile(r'R\d')
        read_arr = filter(regex.search, self.__dict__.keys())
        cat_arr = np.array([getattr(self, x) for x in read_arr]).transpose().flatten()
        absent = [x for x in cat_arr if not os.path.exists(x)]

        assert (len(absent) == 0), "ValueError: scito.ScitoSamples.from_df(). FASTQ files {} do not exist".format(absent)
        self.fastqs = cat_arr

        # TODO need some QA on the df





