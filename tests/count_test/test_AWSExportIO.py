from unittest import TestCase
from scito_count.AWSExportIO import BUSToolsExport, BlockByteExport
from scito_count.S3Interface import S3Interface
from scito_count.BUSTools import BUSTools
from scito_count.BitHeader import BUSHeaderAdtAtac
from scito_count.BlocksIO import BlocksIO
from scito_count.BlockSplit import BlockSplit
from scito_count.BlockByte import BlockByte
from scito_count.SeqFile import FQFile
from scito_count.ProcessSettings import S3Settings, ReadSettings
from scito_count.SeqSync import FQSyncTwoReads
from scito_count.BitFile import BUSFileAdtAtac

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

test_s3_set = S3Settings(conf, "BUSTOOLS TEST")

io_s3_set = S3Settings(conf, "IO TEST FQ")


class TestAWSExportIO(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))
        self.vcr = self.ufixtures.sanitize(attributes=['(?i)token', 'Author', 'User', '(?i)kms'],
                                           targets=[
                                               'arn:aws:sqs:us-west-2:\d+', 'us-west-2.queue.amazonaws.com/\d+',
                                               '3A\d+', '2F\d+', ':\d+:', '\"sg-.*\"', '\"subnet-.*\"',
                                               '\"vpc-.*\"'
                                           ])
        with self.vcr.use_cassette('AWSExportIO_setUp.yml'):
            ground = FQFile(s3_settings=upl_test_s3, read_settings=upl_test_read, byte_range="0-1000", qc_scale="phred")
            async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3, byte_range="0-1000", qc_scale="phred")
            self.sync_two_reads = FQSyncTwoReads((ground, async_file))
            self.sync_two_reads.two_read_sync()
            self.bus_file_adt_atac = BUSFileAdtAtac(self.sync_two_reads)
            self.bus_file_adt_atac.bus_file_stream()
            adt_atac_bus_header = BUSHeaderAdtAtac()
            self.header = adt_atac_bus_header.output_header()
            self.native_bus_tools = BUSTools(bus_header=self.header, bus_records=self.bus_file_adt_atac.bit_records)
            self.native_bus_tools.run_pipe([self.native_bus_tools.bus_sort()])

    def test_bus_tools_export(self):
        with self.vcr.use_cassette('AWSExportIO_bus_tools_export.yml'):
            bt_export = BUSToolsExport(s3_settings=s3_set2)
            bt_export.processed_bus_upload_s3(byte_seq=self.native_bus_tools.processed_bus_file)
            lol = S3Interface(test_s3_set.bucket, test_s3_set.object_key, profile_name="gvaihir")
            header = BUSHeaderAdtAtac()
            h = header.output_header()
            test_h = lol.get_bytes_s3(0, 44).read()
        self.assertEqual(h, test_h)

    def test_block_byte_export(self):
        with self.vcr.use_cassette('AWSExportIO_block_byte_export.yml'):
            handle = BlocksIO(io_s3_set, '0-101000')
            handle.get_object_part()
            self.block_split: BlockSplit = BlockSplit(handle)
            lol = BlockByte(self.block_split)
            lol.byte_blocks()
            bb_export = BlockByteExport(s3_settings=io_s3_set, misc_id='0-101000')
            bb_export.block_range_upload_s3(byte_seq=lol.byte_block_gen)

            kk = S3Interface(io_s3_set.bucket, 'anton/scito/mock/fastq/TEST_FASTQ.BLOCK_BYTE.0-101000', profile_name="gvaihir")
            test_kk = kk.get_bytes_s3(0, 15).read()
        self.assertEqual(struct.unpack('<QQ', test_kk), (0, 7331))
