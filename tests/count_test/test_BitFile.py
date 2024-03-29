from unittest import TestCase
from scito_count.SeqFile import FQFile
from scito_count.ProcessSettings import S3Settings, ReadSettings
from scito_count.SeqSync import FQSyncTwoReads
from scito_count.BitFile import BUSFileAdtAtac
from scito_count.BitRecord import BitRecord

from scito_lambdas.lambda_utils import init_config
import struct
import os
from ufixtures.UfixVcr import UfixVcr

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

s3_set2 = S3Settings(conf, "ATAC ADT R2")
read_set2 = ReadSettings(conf, "ATAC ADT R2")

s3_set3 = S3Settings(conf, "ATAC ADT R3")
read_set3 = ReadSettings(conf, "ATAC ADT R3")

upl_test_s3 = S3Settings(conf, "ATAC ADT R2 UPLOAD TEST")
upl_test_read = ReadSettings(conf, "ATAC ADT R2 UPLOAD TEST")


class TestBUSFileAdtAtac(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)token', 'Author', 'User', '(?i)kms'],
                                           targets=[
                                               'arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                               '3A\d+', '2F\d+', ':\d+:', '\"sg-.*\"', '\"subnet-.*\"',
                                               '\"vpc-.*\"'
                                           ])
        with self.vcr.use_cassette('BUSFileAdtAtac_setUp.yml'):
            ground = FQFile(s3_settings=upl_test_s3, read_settings=upl_test_read, byte_range='0-1000', qc_scale="phred")
            async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3, byte_range='0-1000', qc_scale="phred")
            self.sync_two_reads = FQSyncTwoReads((ground, async_file))
            self.sync_two_reads.two_read_sync()
            self.bus_file_adt_atac = BUSFileAdtAtac(self.sync_two_reads)

    def test_bus_file_stream_adt_atac(self):
        self.bus_file_adt_atac.bus_file_stream()
        bit_rec = BitRecord()
        bc = bit_rec.dna_to_twobit('TCGTCGGCAGCGTCAGCTGGA')
        umi = bit_rec.dna_to_twobit('CCTTTAAG')
        seq = bit_rec.dna_to_twobit('GCTAT')
        pack = struct.pack('<QQLLLL', bc, umi, seq, 1, 0, 0)
        lol = next(self.bus_file_adt_atac.bit_records)
        self.assertEqual(lol, pack)
