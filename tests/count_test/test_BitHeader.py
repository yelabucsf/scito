from unittest import TestCase
import struct
from scito_count.BitHeader import *

class TestAdtAtacBusHeader(TestCase):
    def setUp(self) -> None:
        self.adt_atac_bus_header = AdtAtacBusHeader()

    def test_output_adt_atac_header(self):
        header = self.adt_atac_bus_header.output_adt_atac_header()
        magic = struct.unpack('<4c', header[:4])
        version = struct.unpack('<L', header[4:8])
        bc_len = struct.unpack('<L', header[8:12])
        self.assertEqual(bc_len[0], 21)
