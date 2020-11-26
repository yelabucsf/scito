from unittest import TestCase
from scito_count.SeqExport import *
from scito_count.SeqSync import *

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


class TestNativeBusTools(TestCase):
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

    def test_run_pipe_text(self):
        self.native_bus_tools = NativeBusTools(bus_header=self.header, bus_records=self.bus_file_adt_atac.bit_records)
        self.native_bus_tools.run_pipe([self.native_bus_tools._bus_text()])
        self.assertEqual(self.native_bus_tools.processed_bus_file[:21].decode(), 'TCGTCGGCAGCGTCAGCTGGA')

    def test_run_pipe_sort(self):
        self.native_bus_tools = NativeBusTools(bus_header=self.header, bus_records=self.bus_file_adt_atac.bit_records)
        self.native_bus_tools.run_pipe([self.native_bus_tools.bus_sort(),
                                        self.native_bus_tools._bus_text()])
        self.assertEqual(self.native_bus_tools.processed_bus_file[:21].decode(), 'TCGTCGGCAGCGTCAGACACA')
