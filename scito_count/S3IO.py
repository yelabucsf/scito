from scito_count.SeqArranger import *
from scito_count.ProcessSettings import *
from scito_count.BitFile import *
from scito_count.S3Interface import S3Interface
from scito_count.BUSTools import *
from scito_utils.S3InterfaceGen import *
from io import BytesIO
import os

'''
Class to upload binary data to s3
'''

class S3IO(object):
    __slots__ = 's3_settings', 'misc_id'
    def __init__(self, s3_settings, misc_id=''):
        '''
        :param s3_settings: S3Settings object
        :param misc_id: additional ID to append to the basename of the S3 key
        '''
        self.s3_settings = s3_settings
        self.misc_id = misc_id

    @classmethod
    def s3_upload(cls, file_type: str, encoding: str):
        def s3_upload_inner(func_of_format):
            @functools.wraps(func_of_format)
            def s3_upload_wrapper(self, byte_seq, *args, **kwargs):
                '''
                :param byte_seq: generator of byte strings or full byte string
                '''
                interface_gen = S3InterfaceGen(self.s3_settings, file_type, self.misc_id)
                new_interface = interface_gen.new_key()
                para_file = BytesIO()
                func_of_format(self, byte_seq, para_file, *args, **kwargs)
                para_file.seek(0)
                new_interface.s3_obj.upload_fileobj(
                    para_file,
                    {'ContentType': file_type, 'ContentEncoding': encoding,
                     'ServerSideEncryption': 'aws:kms', 'SSEKMSKeyId': 'alias/managed-s3-key'})
                if not para_file.closed:
                    para_file.close()

            return s3_upload_wrapper
        return s3_upload_inner



class BUSToolsExport(S3IO):
    @S3IO.s3_upload(file_type='SORTED_BUS', encoding='bus')
    def processed_bus_upload(self, byte_seq, para_file):
        para_file.write(byte_seq)


class BlockByteExport(S3IO):
    @S3IO.s3_upload(file_type='BLOCK_BYTE', encoding='(int64, int64)')
    def block_range_upload(self, byte_seq, para_file):
        for read_block in byte_seq:
            para_file.write(read_block)