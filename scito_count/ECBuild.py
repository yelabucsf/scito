import re
import os
from typing import Dict, Tuple
from scito_count.BitRecord import BitRecord
from scito_count.S3Interface import S3Interface


class ECBuildError(Exception):
    """Errors corresponding to misuse of ECBuild"""


class ECBuild(object):
    def __init__(self, config: Dict):
        section = config[list(config.keys())[0]]
        self.s3_interface = S3Interface(section['bucket'],
                                        section['feature map'])
        self.map_names = ['ec_map.tsv', 'tx_map.tsv', 'gene_map.tsv']

    def prepare_maps(self, outdir: str) -> None:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        map_generators = self._construct_maps()
        for prep_process in zip(self.map_names, map_generators):
            outfile = os.path.join(outdir, prep_process[0])
            self._write_map(prep_process[1], outfile)

    def _serve_features(self) -> str:
        features_from_s3 = self.s3_interface.s3_obj.get()["Body"].read().decode('utf-8')
        for feature in features_from_s3.split('\n'):
            if feature is []:
                StopIteration()
            else:
                yield feature

    def _construct_maps(self, sep: str = '\t') -> Tuple:
        bit_record = BitRecord()
        features = self._serve_features()
        for feature_id, feature in enumerate(features):
            after_split = feature.split(sep)
            if not self._is_dna(after_split[0]):
                raise ECBuildError(f'ECBuild.build_ec_map(): {after_split[0]} is not a DNA string')
            equivalence_class = bit_record.dna_to_twobit(after_split[0])
            ec_map_entry = f'{equivalence_class}\t{feature_id}\n'
            transcript_entry = f'{after_split[1]}\n'
            transcript_to_gene_entry = f'{after_split[1]}\t{after_split[1]}\n'
            yield ec_map_entry, transcript_entry, transcript_to_gene_entry



    @staticmethod
    def _is_dna(dna_str: str) -> bool:
        if dna_str is '':
            answer = False
        else:
            answer = bool(re.search("[ATGCN]{%s}" % len(dna_str), dna_str.upper()))
        return answer

    @staticmethod
    def _write_map(map_generator, outfile: str) -> None:
        with open(outfile, 'w') as file_stream:
            for map_entry in map_generator:
                file_stream.write(map_entry)
