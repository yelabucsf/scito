from unittest import TestCase
import os
from scito_count.BlockCatalog import BlockCatalog
from scito_count.ContentTable import ContentTable
from scito_count.ContentTablesIO import ContentTablesIO
from scito_count.ProcessSettings import S3Settings
from scito_lambdas.lambda_utils import init_config

curr_dir = os.path.dirname(os.path.realpath(__file__))
conf = init_config(os.path.join(curr_dir, 'fixtures/test_config.ini'))

class TestBlockCatalog(TestCase):
    def setUp(self) -> None:
        s3_set = S3Settings(conf, "IO TEST FQ")
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
