from unittest import TestCase
from scito_count.SeqFile import *



class TestFastqFile(TestCase):
    def setUp(self, s3_bucket="ucsf-genomics-prod-project-data",
              s3_object_key="anton/scito/mock/fastq/downsamp/seed100_ADT_own_S19_L003_R2_001.fastq.gz",
              config_file=None) -> None:
    def test_import_record_fastq(self):
        self.fail()




class TestFQAdtAtac(TestCase):
    def setUp(self) -> None:
        self.FQAdtAtac = FQAdtAtac()

    def test_parse_adt_atac(self):
        read_block = ["@identifier", "AGGACNATNTAACNCTANTNTCTANCTANTNC", "+", "D:KGAPOJGPADOSJADF:LOGJAFOPJ:LOJDC"]
        self.FQAdtAtac.parse_adt_atac(read_block=read_block, read_start=0, read_end=16)

        print("!!!!!{}".format([self.FQAdtAtac.seq, self.FQAdtAtac.quality_score]))
        self.assertEqual(self.FQAdtAtac.seq, "AGGACNATNTAACNCTANTNTCTANCTANTNC"[:16])