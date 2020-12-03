from scito_count.BlockSplit import *
from scito_count.BlockCatalog import *
from scito_count.S3Interface import *
from scito_count.ProcessSettings import *
from scito_count.SeqExport import *
import struct
from io import BytesIO
import os

'''
Class to import ranges of bytes from s3 directly to RAM
'''

class BlocksIO(object):
    __slots__ = 'block_start', 'block_end', 's3_interface', 'data_stream'
    def __init__(self, s3_settings: S3Settings, byte_range: str):
        '''
        :param byte_range: comes from an SQS. Format "start-end"
        '''
        self.block_start, self.block_end = [int(x) for x in byte_range.split("-")]
        self.s3_interface: S3Interface = S3Interface(s3_settings.bucket, s3_settings.object_key, s3_settings.profile)
        self.data_stream = BytesIO()

    def get_object_part(self):
        self.data_stream.write(self.s3_interface.get_bytes_s3(self.block_start, self.block_end).read())
        self.data_stream.seek(0)

    def close(self):
        self.data_stream.close()



class BlockRangeExport(object):
    def __init__(self, block_split):
        '''
        :param block_split: BlockSplit type
        '''
        self.block_generator = block_split.generate_blocks()

    def byte_blocks(self):
        self.byte_block_gen = self._byte_blocks()

    def _byte_blocks(self):
        for block_start, block_end in self.block_generator:
            byte_string = struct.pack('<QQ', block_start, block_end)
            yield byte_string


"""
class CatalogExport(SeqExport):
    def __init__(self, catalog: BlockCatalog):
        ...

    def catalog_s3_upload(self, s3_settings: S3Settings):
        new_s3_key = "/".join([os.path.dirname(s3_settings.object_key),
                               "CATALOG_"+os.path.basename(s3_settings.object_key)])
        s3_interface: S3Interface = S3Interface(s3_settings.bucket, new_s3_key, s3_settings.profile)
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

"""