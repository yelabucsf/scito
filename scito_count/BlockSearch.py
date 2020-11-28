import struct

'''
Class searches starting of the BGZF header in a blindly split file
'''

class BlockSearch(object):
    def __init__(self, handle):
        self.handle = handle
        self._bgzf_magic = b'\x1f\x8b\x08\x04'


    def header_search(self):
        search_step = 100
        overlap = 10
        curr_position = 0
        header_position = -1
        while header_position == -1:
            probe = self.handle.read(search_step)
            if probe == b'':
                raise StopIteration('BlockSearch.header_search(): header was not detected after complete file.'
                                    'Current file has no BGZF blocks.')
            header_position = probe.find(self._bgzf_magic)
            curr_position += search_step-overlap
            self.handle.seek(curr_position)
        if curr_position > int(65e3):
            raise StopIteration('BlockSearch.header_search(): header was not detected after reading 64 kB of data.'
                                'Current file has no BGZF blocks.')
        return header_position + curr_position - (search_step - overlap)






