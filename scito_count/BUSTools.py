import subprocess as sp
from io import BytesIO
from scito_count.BitFile import *
from typing import List
from warnings import warn


class BUSTools(object):
    __slots__ = 'bus_file', 'processed_bus_file'

    def __init__(self, bus_header: bytes, bus_records: BitFile):
        self.bus_file = BytesIO()
        self.bus_file.write(bus_header)
        for read_block in bus_records:
            self.bus_file.write(read_block)
        self.bus_file.seek(0)

    def run_pipe(self, cmds: List[str]):
        curr_process = sp.Popen(cmds[0].split(" "), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
        self.processed_bus_file = curr_process.communicate(input=self.bus_file.getvalue())[0]
        self.bus_file = 'Deleted input after processing'
        for curr_step in cmds[1:]:
            curr_process = sp.Popen(curr_step.split(" "), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            self.processed_bus_file = curr_process.communicate(input=self.processed_bus_file)[0]

    @staticmethod
    def _bus_correct(whitelist: str):
        warn("WARNING! NativeBusTools._bus_correct(): function is not recommended for performance issues")
        return f'bustools correct -w {whitelist}'

    @staticmethod
    def _bus_text():
        return f'bustools text -p -'

    @staticmethod
    def bus_sort(threads: int = 1,
                 memory: int = None):  # ToDo implement memory cap
        return f'bustools sort -T ./ -t {threads} -p -'

    @staticmethod
    def bus_count(gene_map: str,
                  ec_map: str,
                  tx_names: str):
        return f'bustools count {gene_map} {ec_map} {tx_names}'
