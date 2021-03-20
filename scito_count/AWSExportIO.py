from scito_utils.S3InterfaceGen import *
from io import BytesIO
import os

'''
Class to upload binary data to s3
'''


class AWSExportIO(object):
    __slots__ = 'file_type', 's3_interface'

    def __init__(self, s3_settings, file_type, misc_id=''):
        '''
        :param s3_settings: S3Settings object
        :param file_type: passed
        :param misc_id: additional ID to append to the basename of the S3 key
        '''
        self.file_type = file_type
        interface_gen = S3InterfaceGen(s3_settings, file_type, misc_id)
        self.s3_interface = interface_gen.new_key()

    @classmethod
    def s3_upload(cls, encoding: str):
        def s3_upload_inner(func_of_format):
            @functools.wraps(func_of_format)
            def s3_upload_wrapper(self, byte_seq, *args, **kwargs):
                '''
                :param byte_seq: generator of byte strings or full byte string
                '''
                para_file = BytesIO()
                func_of_format(self, byte_seq, para_file, *args, **kwargs)
                para_file.seek(0)
                self.s3_interface.s3_obj.upload_fileobj(
                    para_file,
                    {'ContentType': self.file_type, 'ContentEncoding': encoding,
                     'ServerSideEncryption': 'aws:kms',
                     'SSEKMSKeyId': 'alias/managed-s3-key'})  # todo get KMS keys from the API
                if not para_file.closed:
                    para_file.close()

            return s3_upload_wrapper

        return s3_upload_inner

    @classmethod  # TODO test this when EFS is allowed
    def efs_upload(cls, func_of_format):
        @functools.wraps(func_of_format)
        def efs_upload_wrapper(self, byte_seq, outdir, *args, **kwargs):
            '''
            :param byte_seq: generator of byte strings or full byte string
            :param outdir: defined by lambda when creating local mount point
            '''
            new_filename = os.path.basename(self.s3_interface.s3_obj.key)
            out_file = os.path.join(outdir, new_filename)
            para_file = BytesIO()
            func_of_format(self, byte_seq, outdir, para_file, *args, **kwargs)
            para_file.seek(0)
            with open(out_file, 'wb') as f:
                f.write(para_file)
            if not para_file.closed:
                para_file.close()

        return efs_upload_wrapper


class BUSToolsExport(AWSExportIO):
    def __init__(self, s3_settings, file_type='SORTED_BUS', misc_id=''):
        super().__init__(s3_settings, file_type, misc_id)
        if file_type != 'SORTED_BUS':
            raise ValueError('BUSToolsExport(): default file_type must be kept as SORTED_BUS')

    @AWSExportIO.s3_upload(encoding='bus')
    def processed_bus_upload_s3(self, byte_seq, para_file):
        para_file.write(byte_seq)

    @AWSExportIO.efs_upload
    def processed_bus_upload_efs(self, byte_seq, outdir, para_file):
        para_file.write(byte_seq)


class BlockByteExport(AWSExportIO):
    def __init__(self, s3_settings, file_type='BLOCK_BYTE', misc_id=''):
        super().__init__(s3_settings, file_type, misc_id)
        if file_type != 'BLOCK_BYTE':
            raise ValueError('BlockByteExport(): default file_type must be kept as BLOCK_BYTE')

    @AWSExportIO.s3_upload(encoding='(int64, int64)')
    def block_range_upload_s3(self, byte_seq, para_file):
        for read_block in byte_seq:
            para_file.write(read_block)
