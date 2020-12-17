import os
import functools
from io import BytesIO
from scito_utils.S3InterfaceGen import *


class EFSIO(object):
    def __init__(self, outdir, misc_id=''):
        if not os.path.exists(outdir):
            raise ValueError("EFSIO(): provided output directory does not exist")
        self.outdir = outdir
        self.misc_id = misc_id

    @classmethod
    def efs_upload(cls, file_type: str):
        def efs_upload_inner(func_of_format):
            @functools.wraps(func_of_format)
            def efs_upload_wrapper(self, byte_seq, *args, **kwargs):
                '''
                :param byte_seq: generator of byte strings or full byte string
                '''
                new_filename = ... # ToDo implement new file name for export
                out_file = os.path.join(self.outdir, new_filename)
                para_file = BytesIO()
                func_of_format(self, byte_seq, para_file, *args, **kwargs)
                para_file.seek(0)
                with open(out_file, 'wb') as f:
                    f.write(para_file)
                if not para_file.closed:
                    para_file.close()

            return efs_upload_wrapper
        return efs_upload_inner


class BUSToolsExport(EFSIO):
    @EFSIO.s3_upload(file_type='SORTED_BUS', encoding='bus')
    def processed_bus_upload(self, byte_seq, para_file):
        para_file.write(byte_seq)


class BlockByteExport(EFSIO):
    @EFSIO.s3_upload(file_type='BLOCK_BYTE', encoding='(int64, int64)')
    def block_range_upload(self, byte_seq, para_file):
        for read_block in byte_seq:
            para_file.write(read_block)
