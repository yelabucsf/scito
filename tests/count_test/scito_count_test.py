from unittest import TestCase
from scito_count import SeqFile


class TestHoplites(TestCase):

    def setUp(self, run=9):
        meta = pd.DataFrame({"well_id": list(range(1)),
                             "TCR": sorted(glob("../mock_data/nero.Hoplites/run{}/outs/".format(run)))})
        self.hop = Hoplites(meta=meta)


class TestHop(TestHoplites):
    def test__import_data(self):
        out = self.hop._import_data("TCR")
        self.assertEqual(len(out["clonotypes_all"]), 1)
        self.assertEqual(out["clonotypes_all"][0].columns[0], "clonotype_id")
        self.assertEqual(len(out["contigAnno_all"]), 1)
        self.assertEqual(out["contigAnno_all"][0].columns[0], "barcode")
