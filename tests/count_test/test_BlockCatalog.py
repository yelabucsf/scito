from unittest import TestCase
from scito_count.BlockCatalog import *
from scito_count.ProcessSettings import *
from scito_count.ContentTable import *

s3_set = S3Settings("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini",
                    "IO TEST FQ")

class TestBlockCatalog(TestCase):
    def setUp(self) -> None:
        self.content_tab_gen = ContentTablesIO(s3_set)
        self.content_tab_gen.content_table_stream()
        self.fq_adt_atac_catalog = BlockCatalog(n_parts=4)

    def test_create_catalog(self):
        lol = ContentTable(self.content_tab_gen)
        self.fq_adt_atac_catalog.create_catalog(content_table=lol.content_table_arr, overlap=0)
        list_lol = self.fq_adt_atac_catalog.ranges
        self.assertEqual(list_lol[0][1], 29576)
        self.assertEqual(len(list_lol), 4)
