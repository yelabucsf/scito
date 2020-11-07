from unittest import TestCase
from scito_count.SeqExport import *
from scito_count.ProcessSettings import *
from scito_count.SeqArranger import *
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




class TestFQExport(TestCase):
    def setUp(self) -> None:
        pass

    def test_s3_upload_r2(self):
        read2 = FQFile(s3_settings=s3_set2, read_settings=read_set2, qc_scale="phred")
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        dict_reads = {"read2": read2,
                      "read3": read3}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
        self.sync_two_reads.two_read_sync()
        self.fq_seq_arranger_adt_atac = FQSeqArrangerAdtAtac(self.sync_two_reads)
        self.seq_export_arr_r2 = FQExport(self.fq_seq_arranger_adt_atac)
        self.seq_export_arr_r2.fq_s3_upload(s3_settings=s3_set2)

        uploaded_r2 = FQFile(s3_settings=upl_test_s3, read_settings=upl_test_read, qc_scale="phred")
        uploaded_r2.import_record_fastq()
        lol = next(uploaded_r2.read_records)
        self.assertEqual(lol.seq, "TCGTCGGCAGCGTCAGCTGGA")
        self.assertTrue(issubclass(type(uploaded_r2), SeqFile))
        self.assertFalse(issubclass(type(uploaded_r2), List))
        print("!!!!!{}".format(lol.seq))

    def test_s3_upload_r3(self):
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        self.seq_export_r3 = FQExport(read3)
        self.seq_export_r3.fq_s3_upload(s3_settings=s3_set3)
        self.assertEqual(1, 2 - 1)  # dummy test


    def test_bus_s3_upload(self):
        read2 = FQFile(s3_settings=upl_test_s3, read_settings=upl_test_read, qc_scale="phred")
        read3 = FQFile(s3_settings=s3_set3, read_settings=read_set3, qc_scale="phred")
        dict_reads = {"read2": read2,
                      "read3": read3}
        self.sync_two_reads = FQSyncTwoReads(dict_reads, 'read2')
        self.sync_two_reads.two_read_sync()
        self.bus_file_adt_atac = BUSFileAdtAtac(self.sync_two_reads)
        self.bus_file_adt_atac.bus_file_stream_adt_atac()
        self.adt_atac_bus_header = BUSHeaderAdtAtac()
        header = self.adt_atac_bus_header.output_adt_atac_header()
        to_export = BUSExport(reads_object=self.bus_file_adt_atac, header=header)
        to_export.bus_s3_upload(s3_settings=s3_set3)
        self.assertEqual(1, 2 - 1)  # dummy test
