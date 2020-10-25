from scito_count.BlockCatalog import *
from scito_count.ProcessSettings import *
import os

class CatalogExport(object):
    def __init__(self, catalog: BlockCatalog):
        self.catalog = catalog

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

