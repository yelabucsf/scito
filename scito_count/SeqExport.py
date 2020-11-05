from scito_count.SeqFile import *
from scito_count.SeqArranger import *
from scito_count.ProcessSettings import *
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
        if issubclass(type(reads_object), SeqFile):
            self.reads_to_export = reads_object.read_records
        elif issubclass(type(reads_object), SeqArranger): #
            self.reads_to_export = reads_object.arrange_sequences()
        else:
            raise TypeError("SeqExport(): Unknown file format")

    def s3_upload(self, s3_settings: S3Settings, verbose=False):
        new_s3_key = "/".join([os.path.dirname(s3_settings.object_key),
                               "READY_"+os.path.basename(s3_settings.object_key)])
        s3_interface: S3Interface = S3Interface(s3_settings.bucket, new_s3_key, s3_settings.profile)
        if verbose:
            print("Starting upload to {s3_settings.object_key}")
        para_file = BytesIO()
        with gzip.GzipFile(fileobj=para_file, mode='wb') as gz:
            for read_block in self.reads_to_export:
                new_lines = read_block.fq_block_to_text()
                gz.write(new_lines.encode())
        para_file.seek(0)
        s3_interface.s3_obj.upload_fileobj(
            para_file,
            {'ContentType': str(type(self.reads_to_export)), 'ContentEncoding': 'gzip',
             'ServerSideEncryption': 'aws:kms', 'SSEKMSKeyId': 'alias/managed-s3-key'})

