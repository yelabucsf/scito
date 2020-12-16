from unittest import TestCase
from scito_count.S3IO import *
from scito_count.BitHeader import *
from scito_count.BlocksIO import BlocksIO
from scito_count.BlockSplit import *
from scito_count.BlockByte import *
import struct



s3_set2 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R2")
read_set2 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2")
s3_set3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                     "ATAC ADT R3")
read_set3 = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R3")


upl_test_s3 = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "ATAC ADT R2 UPLOAD TEST")
upl_test_read = ReadSettings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                             "ATAC ADT R2 UPLOAD TEST")


test_s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                         "BUSTOOLS TEST")

io_s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST FQ")


class TestS3IO(TestCase):
    def setUp(self) -> None:
        ground = FQFile(s3_settings=upl_test_s3, read_settings=upl_test_read, qc_scale="phred")
        async_file = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        dict_reads = {"read2": ground,
                      "read3": async_file}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
        self.sync_two_reads.two_read_sync()
        self.bus_file_adt_atac = BUSFileAdtAtac(self.sync_two_reads)
        self.bus_file_adt_atac.bus_file_stream_adt_atac()
        adt_atac_bus_header = BUSHeaderAdtAtac()
        self.header = adt_atac_bus_header.output_adt_atac_header()
        self.native_bus_tools = BUSTools(bus_header=self.header, bus_records=self.bus_file_adt_atac.bit_records)
        self.native_bus_tools.run_pipe([self.native_bus_tools.bus_sort()])

    def test_bus_tools_export(self):
        bt_export = BUSToolsExport(s3_settings=s3_set2)
        bt_export.processed_bus_upload(byte_seq=self.native_bus_tools.processed_bus_file)
        lol = S3Interface(test_s3_set.bucket, test_s3_set.object_key, test_s3_set.profile)
        header = BUSHeaderAdtAtac()
        h = header.output_adt_atac_header()
        test_h = lol.get_bytes_s3(0, 44).read()
        self.assertEqual(h, test_h)


    def test_block_byte_export(self):
        handle = BlocksIO(io_s3_set, '0-101000')
        handle.get_object_part()
        self.block_split: BlockSplit = BlockSplit(handle)
        lol = BlockByte(self.block_split)
        lol.byte_blocks()
        bb_export = BlockByteExport(s3_settings=io_s3_set, misc_id='0-101000')
        bb_export.block_range_upload(lol.byte_block_gen)

        kk = S3Interface(io_s3_set.bucket, 'anton/scito/mock/fastq/TEST_FASTQ.BLOCK_BYTE.0-101000', io_s3_set.profile)
        test_kk = kk.get_bytes_s3(0, 15).read()
        self.assertEqual(struct.unpack('<QQ', test_kk), (0,7331))
