from scito_count.SeqArranger import *
from scito_count.ProcessSettings import *
from scito_count.BitFile import *
from scito_count.S3Interface import S3Interface
from io import BytesIO
import os


class SeqExport(object):
    __slots__ = "reads_to_export"
    def __init__(self, reads_object):
        '''
        :param reads_object: generator.ReadRecord. Accepts SeqFile or generator.ReadArranger.
        If SeqFile - keeps only attribute read_records. If ReadArranger - keeps entire object. Both resolve to ReadRecord's
        '''
        if issubclass(type(reads_object), (SeqFile, SeqArranger)):
            self.reads_to_export = reads_object.read_records
        elif issubclass(type(reads_object), BitFile):
            self.reads_to_export = reads_object.bit_records
        else:
            raise TypeError("SeqExport(): Unknown file format")

    @classmethod
    def s3_upload(cls, file_type: str, encoding: str):
        def s3_upload_inner(func_of_format):
            @functools.wraps(func_of_format)
            def s3_upload_wrapper(self, s3_settings: S3Settings, *args, **kwargs):
                new_s3_key = "/".join([os.path.dirname(s3_settings.object_key),
                                       f"{file_type.upper()}_"+os.path.basename(s3_settings.object_key)])
                s3_interface: S3Interface = S3Interface(s3_settings.bucket, new_s3_key, s3_settings.profile)
                para_file = BytesIO()
                func_of_format(self, s3_settings, para_file, *args, **kwargs)
                para_file.seek(0)
                s3_interface.s3_obj.upload_fileobj(
                    para_file,
                    {'ContentType': str(type(self.reads_to_export)), 'ContentEncoding': encoding,
                     'ServerSideEncryption': 'aws:kms', 'SSEKMSKeyId': 'alias/managed-s3-key'})
                if not para_file.closed:
                    para_file.close()

            return s3_upload_wrapper
        return s3_upload_inner

class FQExport(SeqExport):
    @SeqExport.s3_upload(file_type='FQ_READY', encoding='gzip')
    def fq_s3_upload(self, s3_settings, para_file):
        with gzip.GzipFile(fileobj=para_file, mode='wb') as gz:
            for read_block in self.reads_to_export:
                new_lines = read_block.fq_block_to_text()
                gz.write(new_lines.encode())


class BUSExport(SeqExport):
    __slots__ = 'header'
    def __init__(self, reads_object, header: BitHeader):
        super().__init__(reads_object)
        self.header = header

    @SeqExport.s3_upload(file_type='BUS', encoding='bus')
    def bus_s3_upload(self, s3_settings, para_file):
        para_file.write(self.header)
        for read_block in self.reads_to_export:
            para_file.write(read_block)




