import subprocess as sp
from io import BytesIO
from scito_count.BitHeader import *
from scito_count.BitFile import *
from typing import List

class NativeBusTools(object):
    def __init__(self, bus_header: BUSHeader, bus_records: BUSFile):
        self.bus_file = BytesIO()
        self.bus_file.write(bus_header)
        for read_block in bus_records:
            self.bus_file.write(read_block)


    def _run_pipe(self, cmds: List[str]):
        prev_process: None = None
        for step in cmds:
            curr_process: sp.Popen = sp.Popen(step.split(" "), stdin=prev_process, stdout=sp.PIPE, stderr=sp.PIPE)
            prev_process: sp.Popen = curr_process
            curr_process.wait()
            returncode = curr_process.returncode
            if returncode == -1:
                stderr = curr_process.stderr.read()
                raise RuntimeError(f"NativeBusTools._run_pipe(): BUStools exited with error: {stderr}")

    def bus_correct_sort(self,
                 whitelist: str,
                 in_file: str,
                 out_file: str,
                 n_threads: int):
        corrector = f"bustools correct -w {whitelist} -p {in_file}"
        sorter = f"bustools sort -t {n_threads} -o {out_file}"
        self._run_pipe([corrector, sorter])




