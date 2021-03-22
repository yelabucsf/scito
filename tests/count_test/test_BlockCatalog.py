from unittest import TestCase

from scito_count.BlockCatalog import BlockCatalog
from scito_count.ContentTable import ContentTable
from scito_count.ContentTablesIO import ContentTablesIO
from scito_lambdas.lambda_utils import *


class TestBlockCatalog(TestCase):
    def setUp(self) -> None:
        config = init_config("/Users/antonogorodnikov/Documents/Work/Python/scito/tests/config_test.ini")
        s3_set = S3Settings(config, "IO TEST FQ")
        self.content_tab_gen = ContentTablesIO(s3_set)
        self.content_tab_gen.content_table_stream()
        self.fq_adt_atac_catalog = BlockCatalog(n_parts=4)

    def test_create_catalog(self):
        lol = ContentTable(self.content_tab_gen)
        self.fq_adt_atac_catalog.create_catalog(content_table=lol.content_table_arr, overlap=0)
        list_lol = self.fq_adt_atac_catalog.ranges
        self.assertEqual(list_lol[0][1], 29576)
        self.assertEqual(len(list_lol), 4)

    def test_create_catalog_overlap(self):
        lol = ContentTable(self.content_tab_gen)
        self.fq_adt_atac_catalog.create_catalog(content_table=lol.content_table_arr, overlap=1)
        list_lol = self.fq_adt_atac_catalog.ranges
        self.assertEqual(list_lol[0][1], 36974)
        self.assertEqual(len(list_lol), 4)
