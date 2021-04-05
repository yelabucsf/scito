import numpy as np
from scito_lambdas.lambda_utils import init_config
from unittest import TestCase
from ufixtures.UfixVcr import UfixVcr
from scito_count.ECBuild import *

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

class TestECBuild(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                           targets=['arn:aws:sqs:us-west-2:\d+'])
        self.ec_build = ECBuild(config=conf)

    def test_prepare_maps(self):
        with self.vcr.use_cassette('ECBuild_prepare_maps.yml'):
            self.ec_build.prepare_maps(outdir=os.path.join(curr_dir, "fixtures/maps"))
        ec = []
        with open(os.path.join(curr_dir, "fixtures/maps", "ec_map.tsv"), 'r') as ec_map:
            for line in ec_map:
                ec.append(line.strip().split('\t'))
        self.assertEqual(len(ec), 60)
        self.assertEqual(ec[0], ['627', '0'])

        genes = []
        with open(os.path.join(curr_dir, "fixtures/maps", "gene_map.tsv"), 'r') as gene_map:
            for line in gene_map:
                genes.append(line.strip().split('\t'))
        self.assertEqual(len(genes), 60)
        self.assertEqual(genes[0], ['CD45', 'CD45'])


    def test__serve_features(self):
        with self.vcr.use_cassette('ECBuild__serve_features.yml'):
            feat_generator = self.ec_build._serve_features()
            test = next(feat_generator)
        self.assertTrue(isinstance(test, str))
        self.assertEqual(test, 'GCTAT\tCD45')


    def test__construct_maps(self):
        with self.vcr.use_cassette('ECBuild__construct_maps.yml'):
            maps = self.ec_build._construct_maps(sep='\t')
            entries = [next(x) for x in maps]
        [self.assertTrue(isinstance(x, str)) for x in entries]
        self.assertEqual(entries, ['627\t0\n', 'CD45\n', 'CD45\tCD45\n'])


    def test__is_dna(self):
        self.assertTrue(self.ec_build._is_dna('ANGNANTNTANTACACAAGCAC'))
        self.assertTrue(self.ec_build._is_dna('actgn'))
        self.assertFalse(self.ec_build._is_dna(''))
        self.assertFalse(self.ec_build._is_dna('JFKSDJFA'))


